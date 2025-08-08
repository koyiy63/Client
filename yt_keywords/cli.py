from __future__ import annotations

import json
import os
from typing import List, Optional

import pandas as pd
import typer
from rich import box
from rich.console import Console
from rich.table import Table

from .suggest import get_suggestions
from .trends import interest_over_time, compute_trend_features
from .youtube_api import YouTubeClient
from .score import score_keywords
from .utils import setup_requests_cache

app = typer.Typer(add_completion=False, help="YouTube SEO Keywords Engine")
console = Console()


def _print_table(df: pd.DataFrame, fields: Optional[List[str]] = None, max_rows: int = 50) -> None:
    if df is None or df.empty:
        console.print("[yellow]No data.[/yellow]")
        return
    if fields is None:
        fields = list(df.columns)
    table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
    for col in fields:
        table.add_column(col)
    for _, row in df.head(max_rows).iterrows():
        table.add_row(*[str(row.get(col, "")) for col in fields])
    console.print(table)


@app.command()
def suggest(
    seed: List[str] = typer.Argument(..., help="Seed keyword(s)"),
    region: str = typer.Option("US", help="Region code (GL)"),
    lang: str = typer.Option("en", help="Language (HL)"),
    depth: int = typer.Option(1, help="Expansion depth: 1 = direct, 2 = + a-z0-9, etc."),
    output_format: str = typer.Option("table", "--format", help="Output format: table|json|csv"),
):
    """Get YouTube autocomplete suggestions."""
    setup_requests_cache()
    seeds = seed
    sugg_map = get_suggestions(seeds, lang=lang, region=region, depth=depth)
    rows = []
    for s in seeds:
        for sug in sugg_map.get(s, []):
            rows.append({"seed": s, "suggestion": sug})
    df = pd.DataFrame(rows)
    if output_format == "json":
        console.print_json(json.dumps({"seeds": seeds, "suggestions": sugg_map}, ensure_ascii=False))
    elif output_format == "csv":
        console.print(df.to_csv(index=False))
    else:
        _print_table(df, fields=["seed", "suggestion"], max_rows=200)


@app.command()
def score(
    seed: List[str] = typer.Argument(..., help="Keyword(s) to score"),
    region: str = typer.Option("US", help="Region code (GL)"),
    lang: str = typer.Option("en-US", help="Language for trends (HL)"),
    depth: int = typer.Option(1, help="Suggestion expansion depth for demand proxies"),
    max_results: int = typer.Option(20, help="Max top results to sample via API"),
    use_api: bool = typer.Option(True, help="Use YouTube Data API if YT_API_KEY is set"),
    output_format: str = typer.Option("table", "--format", help="Output format: table|json|csv"),
    verbose: bool = typer.Option(False, help="Include sub-scores in output table"),
):
    """Score keywords for viral potential (0-100)."""
    setup_requests_cache()

    # Suggestions for demand proxies
    sugg_map = get_suggestions(seed, lang=lang.split("-")[0], region=region, depth=depth)

    # Trends
    trends_df = interest_over_time(seed, geo=region, timeframe="today 12-m", lang=lang)
    trends_features = compute_trend_features(trends_df)

    # Competition via API (optional)
    comp_features = None
    if use_api and os.environ.get("YT_API_KEY"):
        yt = YouTubeClient()
        comp = {}
        for kw in seed:
            comp[kw] = yt.competition_snapshot(kw, region=region, max_results=max_results)
        comp_features = comp

    scored = score_keywords(seed, sugg_map, trends_features, comp_features)

    if output_format == "json":
        console.print_json(scored.to_json(orient="records"))
        return
    if output_format == "csv":
        console.print(scored.to_csv(index=False))
        return

    show_cols = ["keyword", "viral_score", "suggest_count", "recent_mean", "median_views_top", "recent_fraction_top"]
    if verbose:
        show_cols += ["explain_demand", "explain_momentum", "explain_competition", "explain_misc"]
    _print_table(scored, fields=show_cols, max_rows=100)


@app.command()
def analyze(
    seed: List[str] = typer.Argument(..., help="Seed keyword(s)"),
    region: str = typer.Option("US", help="Region code (GL)"),
    lang: str = typer.Option("en-US", help="Language for trends (HL)"),
    depth: int = typer.Option(2, help="Suggestion expansion depth"),
    max_results: int = typer.Option(20, help="Max results for API competition"),
    output_format: str = typer.Option("table", "--format", help="Output format: table|json|csv"),
):
    """Full pipeline: suggest + score."""
    setup_requests_cache()
    sugg_map = get_suggestions(seed, lang=lang.split("-")[0], region=region, depth=depth)

    # Select top suggestions per seed as candidates (cap to avoid huge calls)
    candidates: List[str] = []
    for s in seed:
        for sug in sugg_map.get(s, [])[:50]:
            candidates.append(sug)
    # Deduplicate while preserving order
    seen = set()
    candidates = [x for x in candidates if not (x in seen or seen.add(x))]

    # Trends for candidates
    trends_df = interest_over_time(candidates[:5], geo=region, timeframe="today 12-m", lang=lang)  # pytrends caps comparisons
    trends_features = compute_trend_features(trends_df)

    # Competition (optional)
    comp_features = None
    if os.environ.get("YT_API_KEY"):
        yt = YouTubeClient()
        comp = {}
        for kw in candidates[:30]:
            comp[kw] = yt.competition_snapshot(kw, region=region, max_results=max_results)
        comp_features = comp

    scored = score_keywords(candidates, sugg_map, trends_features, comp_features)

    if output_format == "json":
        console.print_json(scored.to_json(orient="records"))
        return
    if output_format == "csv":
        console.print(scored.to_csv(index=False))
        return

    _print_table(scored, fields=["keyword", "viral_score", "suggest_count", "recent_mean", "median_views_top", "recent_fraction_top"], max_rows=100)


if __name__ == "__main__":
    app()