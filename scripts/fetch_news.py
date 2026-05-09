#!/usr/bin/env python3
"""Fetch top financial/market headlines from NewsAPI."""

import os
import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta

def fetch_news():
    api_key = os.environ.get("NEWSAPI_KEY")
    if not api_key:
        print(json.dumps({"error": "NEWSAPI_KEY environment variable not set"}))
        sys.exit(1)

    # Get news from the last 24 hours
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Search for US stock market news
    queries = [
        "US stock market",
        "Wall Street",
        "Federal Reserve",
        "S&P 500 OR Nasdaq OR Dow Jones",
    ]
    
    all_articles = []
    
    for query in queries:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&"
            f"from={yesterday}&"
            f"language=en&"
            f"sortBy=relevancy&"
            f"pageSize=10&"
            f"apiKey={api_key}"
        )
        
        try:
            req = Request(url, headers={"User-Agent": "MarketNewsDigest/1.0"})
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "ok":
                    all_articles.extend(data.get("articles", []))
        except (URLError, HTTPError) as e:
            print(f"Warning: Failed to fetch for query '{query}': {e}", file=sys.stderr)
            continue
    
    # Deduplicate by title
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title = article.get("title", "")
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append({
                "title": title,
                "description": article.get("description", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", ""),
                "publishedAt": article.get("publishedAt", ""),
            })
    
    # Sort by publish date (most recent first) and limit
    unique_articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
    unique_articles = unique_articles[:20]
    
    result = {
        "source": "NewsAPI",
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "article_count": len(unique_articles),
        "articles": unique_articles,
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    fetch_news()
