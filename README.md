# YouTube SEO Keywords Engine

A fast, data-driven CLI (and optional UI) to generate YouTube keyword ideas and score their viral potential using:
- YouTube Autocomplete
- Google Trends (pytrends)
- Optional YouTube Data API v3 (if `YT_API_KEY` is set)

## Install

```bash
python -m pip install -r requirements.txt
```

Optionally set your YouTube Data API key:

```bash
export YT_API_KEY=YOUR_KEY
```

## Quick start

- Suggestions only:
```bash
python -m yt_keywords.cli suggest "ai tutorial" --region US --lang en --depth 2 --format table
```

- Score viral potential:
```bash
python -m yt_keywords.cli score "ai tutorial" "ai tools" --region US --lang en --max-results 20 --format table
```

- Full analysis (suggest + score):
```bash
python -m yt_keywords.cli analyze "ai tutorial" --region US --lang en --depth 2 --max-results 20 --format table
```

Use `--format json` or `--format csv` to export.

## Scoring overview

The engine blends multiple signals into a 0-100 score:
- Trend momentum (Google Trends slope last 4-12 weeks)
- Search demand proxy (autocomplete coverage and breadth)
- Competition (median/upper-quantile views of top results, optional via API)
- Freshness (share of top results published in last 90 days)

Weights are tuned heuristically and shown per keyword in the output when `--verbose`.

## UI (optional)

```bash
streamlit run streamlit_app.py
```

## Notes
- Google Trends returns relative interest (0-100), not absolute volumes.
- Without API key, competition metrics are heuristic.
- Respect quotas and fair-use guidelines.