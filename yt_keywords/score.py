from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from .utils import normalize_scores, safe_divide


def _suggestion_features(seed: str, suggestions: Dict[str, List[str]]) -> Dict[str, float]:
    sug_list = suggestions.get(seed, [])
    num_suggestions = float(len(sug_list))
    unique_token_count = float(len(set(" ".join(sug_list).split()))) if sug_list else 0.0
    avg_len = float(np.mean([len(s) for s in sug_list])) if sug_list else 0.0
    return {
        "suggest_count": num_suggestions,
        "suggest_vocab": unique_token_count,
        "suggest_avg_len": avg_len,
    }


def _trends_features(seed: str, trends: Optional[Dict[str, Dict[str, float]]]) -> Dict[str, float]:
    if not trends or seed not in trends:
        return {
            "trend_slope_4w": 0.0,
            "trend_slope_12w": 0.0,
            "recent_mean": 0.0,
            "recent_peak": 0.0,
            "volatility": 0.0,
        }
    t = trends[seed]
    return {
        "trend_slope_4w": float(t.get("trend_slope_4w", 0.0)),
        "trend_slope_12w": float(t.get("trend_slope_12w", 0.0)),
        "recent_mean": float(t.get("recent_mean", 0.0)),
        "recent_peak": float(t.get("recent_peak", 0.0)),
        "volatility": float(t.get("volatility", 0.0)),
    }


def _competition_features(seed: str, competition: Optional[Dict[str, Dict[str, float]]]) -> Dict[str, float]:
    if not competition or seed not in competition:
        return {
            "median_views_top": 0.0,
            "p75_views_top": 0.0,
            "recent_fraction_top": 0.0,
            "sample_size": 0.0,
        }
    c = competition[seed]
    return {
        "median_views_top": float(c.get("median_views_top", 0.0)),
        "p75_views_top": float(c.get("p75_views_top", 0.0)),
        "recent_fraction_top": float(c.get("recent_fraction_top", 0.0)),
        "sample_size": float(c.get("sample_size", 0.0)),
    }


def score_keywords(
    seeds: Iterable[str],
    suggestions: Dict[str, List[str]],
    trends_features: Optional[Dict[str, Dict[str, float]]] = None,
    competition_features: Optional[Dict[str, Dict[str, float]]] = None,
) -> pd.DataFrame:
    seeds_list = list(dict.fromkeys([s.strip() for s in seeds if s and s.strip()]))

    rows = []
    for seed in seeds_list:
        sug = _suggestion_features(seed, suggestions)
        trn = _trends_features(seed, trends_features)
        cmp = _competition_features(seed, competition_features)
        row = {"keyword": seed, **sug, **trn, **cmp}
        rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # Normalization across the batch
    df["nz_suggest_count"] = normalize_scores(df["suggest_count"], 0, 1)
    df["nz_suggest_vocab"] = normalize_scores(df["suggest_vocab"], 0, 1)
    df["nz_recent_mean"] = normalize_scores(df["recent_mean"], 0, 1)
    df["nz_recent_peak"] = normalize_scores(df["recent_peak"], 0, 1)
    df["nz_trend_slope_4w"] = normalize_scores(df["trend_slope_4w"], 0, 1)
    df["nz_trend_slope_12w"] = normalize_scores(df["trend_slope_12w"], 0, 1)

    # Competition: lower views => easier => invert
    df["nz_median_views_inv"] = [1 - x for x in normalize_scores(df["median_views_top"], 0, 1)]
    df["nz_p75_views_inv"] = [1 - x for x in normalize_scores(df["p75_views_top"], 0, 1)]
    df["nz_recent_fraction_top"] = normalize_scores(df["recent_fraction_top"], 0, 1)

    # Weights (sum to 1.0). Tune as needed.
    w = {
        "demand": 0.40,  # suggestions + trends level
        "momentum": 0.25,  # slopes and peaks
        "competition": 0.25,  # inverted views, recency
        "misc": 0.10,  # buffer
    }

    demand = 0.6 * df["nz_suggest_count"] + 0.4 * df["nz_suggest_vocab"]
    momentum = 0.5 * df["nz_trend_slope_4w"] + 0.5 * df["nz_trend_slope_12w"]
    competition = 0.5 * df["nz_median_views_inv"] + 0.3 * df["nz_p75_views_inv"] + 0.2 * df["nz_recent_fraction_top"]
    misc = 0.5 * df["nz_recent_mean"] + 0.5 * df["nz_recent_peak"]

    composite_0_1 = w["demand"] * demand + w["momentum"] * momentum + w["competition"] * competition + w["misc"] * misc
    df["viral_score"] = (composite_0_1 * 100).round(2)

    # Explanations
    df["explain_demand"] = demand.round(3)
    df["explain_momentum"] = momentum.round(3)
    df["explain_competition"] = competition.round(3)
    df["explain_misc"] = misc.round(3)

    # Sort by score
    df = df.sort_values(by=["viral_score", "suggest_count"], ascending=[False, False]).reset_index(drop=True)
    return df