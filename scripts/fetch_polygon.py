#!/usr/bin/env python3
"""Fetch market news and ticker data from Polygon.io."""

import os
import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta

def fetch_polygon_news():
    api_key = os.environ.get("POLYGON_API_KEY")
    if not api_key:
        print(json.dumps({"error": "POLYGON_API_KEY environment variable not set"}))
        sys.exit(1)

    results = {
        "source": "Polygon.io",
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "news": [],
        "gainers": [],
        "losers": [],
    }

    # Fetch market news
    news_url = (
        f"https://api.polygon.io/v2/reference/news?"
        f"limit=20&"
        f"order=desc&"
        f"sort=published_utc&"
        f"apiKey={api_key}"
    )

    try:
        req = Request(news_url, headers={"User-Agent": "MarketNewsDigest/1.0"})
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            for article in data.get("results", []):
                results["news"].append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "tickers": article.get("tickers", []),
                    "source": article.get("publisher", {}).get("name", "Unknown"),
                    "published_utc": article.get("published_utc", ""),
                    "article_url": article.get("article_url", ""),
                })
    except (URLError, HTTPError) as e:
        print(f"Warning: Failed to fetch Polygon news: {e}", file=sys.stderr)

    # Gainers/losers snapshot requires Polygon paid plan — skip gracefully on free tier
    print("Note: Gainers/losers snapshot requires Polygon paid plan, skipping.", file=sys.stderr)

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    fetch_polygon_news()
