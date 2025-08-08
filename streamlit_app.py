import os
import json
import pandas as pd
import streamlit as st

from yt_keywords.suggest import get_suggestions
from yt_keywords.trends import interest_over_time, compute_trend_features
from yt_keywords.youtube_api import YouTubeClient
from yt_keywords.score import score_keywords
from yt_keywords.utils import setup_requests_cache

st.set_page_config(page_title="YouTube Keywords Engine", page_icon="📈", layout="wide")

setup_requests_cache()

st.title("📈 YouTube SEO Keywords Engine")
seed = st.text_input("Seed keywords (comma-separated)", value="ai tutorial, ai tools")
col1, col2, col3 = st.columns(3)
with col1:
    region = st.text_input("Region (GL)", value="US")
with col2:
    lang = st.text_input("Language (HL)", value="en-US")
with col3:
    depth = st.slider("Suggestion depth", min_value=1, max_value=3, value=2)

if st.button("Run"):
    seeds = [s.strip() for s in seed.split(",") if s.strip()]
    sugg_map = get_suggestions(seeds, lang=lang.split("-")[0], region=region, depth=depth)

    # Candidates from suggestions
    candidates = []
    for s in seeds:
        candidates.extend(sugg_map.get(s, [])[:50])
    seen = set()
    candidates = [x for x in candidates if not (x in seen or seen.add(x))]

    # Trends
    trends_df = interest_over_time(candidates[:5], geo=region, timeframe="today 12-m", lang=lang)
    trends_features = compute_trend_features(trends_df)

    # Competition
    comp_features = None
    if os.environ.get("YT_API_KEY"):
        yt = YouTubeClient()
        comp = {}
        for kw in candidates[:30]:
            comp[kw] = yt.competition_snapshot(kw, region=region, max_results=20)
        comp_features = comp

    scored = score_keywords(candidates, sugg_map, trends_features, comp_features)

    st.subheader("Top Opportunities")
    st.dataframe(scored.head(50))

    with st.expander("Raw suggestions"):
        st.json(sugg_map)

    if not trends_df.empty:
        st.subheader("Google Trends (normalized)")
        st.line_chart(trends_df)