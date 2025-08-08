from __future__ import annotations

import math
import os
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional

import numpy as np
import requests
import requests_cache
from dateutil import parser as date_parser


def setup_requests_cache(cache_name: str = "yt_kw_cache", expire_after_seconds: int = 60 * 30) -> None:
    backend = os.environ.get("REQUESTS_CACHE_BACKEND", "sqlite")
    requests_cache.install_cache(cache_name=cache_name, backend=backend, expire_after=expire_after_seconds)


def normalize_scores(values: Iterable[float], floor: float = 0.0, ceil: float = 1.0) -> List[float]:
    arr = np.array(list(values), dtype=float)
    if arr.size == 0:
        return []
    vmin = np.nanmin(arr)
    vmax = np.nanmax(arr)
    if not math.isfinite(vmin) or not math.isfinite(vmax) or vmin == vmax:
        return [float((floor + ceil) / 2.0)] * arr.size
    scaled = (arr - vmin) / (vmax - vmin)
    return list(np.clip(floor + scaled * (ceil - floor), floor, ceil))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    try:
        if denominator == 0:
            return default
        return float(numerator) / float(denominator)
    except Exception:
        return default


def parse_published_at(iso_timestamp: str) -> Optional[datetime]:
    if not iso_timestamp:
        return None
    try:
        dt = date_parser.isoparse(iso_timestamp)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def compute_recent_days_fraction(published_at_list: List[Optional[datetime]], days: int = 90) -> float:
    now = datetime.now(timezone.utc)
    if not published_at_list:
        return 0.0
    total = len(published_at_list)
    recent = 0
    for dt in published_at_list:
        if dt is None:
            continue
        age_days = (now - dt).days
        if age_days <= days:
            recent += 1
    return safe_divide(recent, total, 0.0)


def robust_median(values: Iterable[float]) -> float:
    arr = np.array([v for v in values if isinstance(v, (int, float)) and math.isfinite(v)], dtype=float)
    if arr.size == 0:
        return 0.0
    return float(np.median(arr))


def robust_percentile(values: Iterable[float], pct: float) -> float:
    arr = np.array([v for v in values if isinstance(v, (int, float)) and math.isfinite(v)], dtype=float)
    if arr.size == 0:
        return 0.0
    pct = max(0.0, min(100.0, pct))
    return float(np.percentile(arr, pct))