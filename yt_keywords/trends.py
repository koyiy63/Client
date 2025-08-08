from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from pytrends.request import TrendReq


def _get_pytrends(lang: str = "en-US", tz: int = 0) -> TrendReq:
    return TrendReq(hl=lang, tz=tz, retries=2, backoff_factor=0.1)


def interest_over_time(keywords: Iterable[str], geo: str = "US", timeframe: str = "today 12-m", lang: str = "en-US") -> pd.DataFrame:
    kws = list(dict.fromkeys([k.strip() for k in keywords if k and k.strip()]))
    if not kws:
        return pd.DataFrame()
    pt = _get_pytrends(lang=lang)
    pt.build_payload(kws, timeframe=timeframe, geo=geo)
    df = pt.interest_over_time()
    if df is None or df.empty:
        return pd.DataFrame()
    if 'isPartial' in df.columns:
        df = df.drop(columns=['isPartial'])
    return df


def _slope_last_n(series: pd.Series, n: int) -> float:
    if series is None or series.empty:
        return 0.0
    s = series.dropna().astype(float)
    if s.size < 3:
        return 0.0
    s_tail = s.tail(min(n, s.size))
    x = np.arange(s_tail.size)
    y = s_tail.values
    x_mean = x.mean()
    y_mean = y.mean()
    denom = ((x - x_mean) ** 2).sum()
    if denom == 0:
        return 0.0
    slope = ((x - x_mean) * (y - y_mean)).sum() / denom
    return float(slope)


def compute_trend_features(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    features: Dict[str, Dict[str, float]] = {}
    if df is None or df.empty:
        return features
    for col in df.columns:
        series = df[col]
        slope_4w = _slope_last_n(series, 4)
        slope_12w = _slope_last_n(series, 12)
        recent_mean = float(series.tail(8).mean()) if series.size >= 8 else float(series.mean())
        overall_mean = float(series.mean()) if series.size > 0 else 0.0
        recent_peak = float(series.tail(12).max()) if series.size >= 12 else float(series.max())
        volatility = float(series.tail(12).std(ddof=0)) if series.size >= 12 else float(series.std(ddof=0))
        features[col] = {
            "trend_slope_4w": slope_4w,
            "trend_slope_12w": slope_12w,
            "recent_mean": recent_mean,
            "overall_mean": overall_mean,
            "recent_peak": recent_peak,
            "volatility": volatility,
        }
    return features