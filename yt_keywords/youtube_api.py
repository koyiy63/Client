from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional, Tuple

import requests

from .utils import parse_published_at, robust_median, robust_percentile, compute_recent_days_fraction


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


class YouTubeClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("YT_API_KEY")

    def _get(self, path: str, params: Dict) -> Dict:
        if not self.api_key:
            raise RuntimeError("YouTube API key not provided. Set YT_API_KEY.")
        url = f"{YOUTUBE_API_BASE}/{path}"
        merged = dict(params)
        merged["key"] = self.api_key
        resp = requests.get(url, params=merged, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def search_videos(self, query: str, region: str = "US", max_results: int = 20, published_after_days: Optional[int] = None) -> List[Dict]:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max(5, min(50, int(max_results))),
            "regionCode": region,
            "order": "relevance",
        }
        if published_after_days is not None:
            dt = datetime.now(timezone.utc) - timedelta(days=int(published_after_days))
            params["publishedAfter"] = dt.isoformat().replace("+00:00", "Z")
        data = self._get("search", params)
        items = data.get("items", [])
        return items

    def get_video_stats(self, video_ids: List[str]) -> List[Dict]:
        if not video_ids:
            return []
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(video_ids[:50]),
        }
        data = self._get("videos", params)
        return data.get("items", [])

    def competition_snapshot(self, keyword: str, region: str = "US", max_results: int = 20) -> Dict[str, float]:
        try:
            search_items = self.search_videos(keyword, region=region, max_results=max_results)
            video_ids = [it["id"]["videoId"] for it in search_items if it.get("id", {}).get("videoId")]
            stats_items = self.get_video_stats(video_ids)
            views = []
            published_at = []
            for it in stats_items:
                stats = it.get("statistics", {})
                view_count = float(stats.get("viewCount", 0)) if stats.get("viewCount") is not None else 0.0
                views.append(view_count)
                published_at.append(parse_published_at(it.get("snippet", {}).get("publishedAt")))
            median_views = robust_median(views)
            p75_views = robust_percentile(views, 75)
            recent_frac = compute_recent_days_fraction(published_at, days=90)
            return {
                "median_views_top": median_views,
                "p75_views_top": p75_views,
                "recent_fraction_top": recent_frac,
                "sample_size": float(len(views)),
            }
        except Exception:
            return {
                "median_views_top": 0.0,
                "p75_views_top": 0.0,
                "recent_fraction_top": 0.0,
                "sample_size": 0.0,
            }