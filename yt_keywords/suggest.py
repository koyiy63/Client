from __future__ import annotations

import asyncio
import json
from typing import Dict, Iterable, List, Optional, Set, Tuple

import aiohttp

SUGGEST_URL = "https://suggestqueries.google.com/complete/search"


async def _fetch_single_suggest(session: aiohttp.ClientSession, query: str, lang: str, region: str) -> List[str]:
    params = {
        "client": "firefox",  # more reliable JSON shape
        "ds": "yt",
        "q": query,
        "hl": lang,
        "gl": region,
    }
    async with session.get(SUGGEST_URL, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        resp.raise_for_status()
        data = await resp.text()
        # Response format: ["query", ["suggestion1", "suggestion2", ...], ...]
        try:
            payload = json.loads(data)
            suggestions = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
            return [s for s in suggestions if isinstance(s, str)]
        except json.JSONDecodeError:
            return []


async def fetch_suggestions_async(seeds: Iterable[str], lang: str = "en", region: str = "US") -> Dict[str, List[str]]:
    unique_seeds = list(dict.fromkeys([s.strip() for s in seeds if s and s.strip()]))
    results: Dict[str, List[str]] = {}
    timeout = aiohttp.ClientTimeout(total=15)
    connector = aiohttp.TCPConnector(limit=20)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [asyncio.create_task(_fetch_single_suggest(session, seed, lang, region)) for seed in unique_seeds]
        suggestions_lists = await asyncio.gather(*tasks, return_exceptions=True)
        for seed, sug in zip(unique_seeds, suggestions_lists):
            if isinstance(sug, Exception):
                results[seed] = []
            else:
                results[seed] = list(dict.fromkeys(sug))
    return results


def _expansion_charset() -> List[str]:
    letters = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    digits = [str(d) for d in range(10)]
    return letters + digits


async def expand_suggestions_async(seed: str, depth: int, lang: str, region: str) -> List[str]:
    collected: Set[str] = set()
    current_layer: Set[str] = {seed}
    timeout = aiohttp.ClientTimeout(total=20)
    connector = aiohttp.TCPConnector(limit=20)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        for d in range(depth):
            next_layer: Set[str] = set()
            tasks = []
            for q in current_layer:
                tasks.append(asyncio.create_task(_fetch_single_suggest(session, q, lang, region)))
                for ch in _expansion_charset():
                    tasks.append(asyncio.create_task(_fetch_single_suggest(session, f"{q} {ch}", lang, region)))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    continue
                for s in res:
                    if s not in collected:
                        collected.add(s)
                        next_layer.add(s)
            current_layer = next_layer
    ordered = list(dict.fromkeys(list(collected)))
    return ordered


def get_suggestions(seeds: Iterable[str], lang: str = "en", region: str = "US", depth: int = 1) -> Dict[str, List[str]]:
    if depth <= 1:
        return asyncio.run(fetch_suggestions_async(seeds, lang=lang, region=region))
    # Expand per seed
    results: Dict[str, List[str]] = {}
    for seed in seeds:
        expanded = asyncio.run(expand_suggestions_async(seed, depth=depth, lang=lang, region=region))
        results[seed] = expanded
    return results