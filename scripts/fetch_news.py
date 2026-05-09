#!/usr/bin/env python3
"""Fetch financial news from free RSS feeds — no API key required."""

import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from xml.etree import ElementTree as ET
from datetime import datetime

RSS_FEEDS = [
    ("Yahoo Finance", "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC,^DJI,^IXIC&region=US&lang=en-US"),
    ("MarketWatch",   "https://feeds.marketwatch.com/marketwatch/topstories/"),
    ("CNBC Markets",  "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("Seeking Alpha", "https://seekingalpha.com/market_currents.xml"),
]

def fetch_rss(name, url):
    articles = []
    try:
        req = Request(url, headers={"User-Agent": "MarketNewsDigest/1.0"})
        with urlopen(req, timeout=15) as resp:
            root = ET.fromstring(resp.read())
        channel = root.find("channel")
        if channel is None:
            return articles
        for item in channel.findall("item")[:8]:
            title = (item.findtext("title") or "").strip()
            if title:
                articles.append({
                    "title": title,
                    "description": (item.findtext("description") or "").strip(),
                    "source": name,
                    "url": (item.findtext("link") or "").strip(),
                    "publishedAt": (item.findtext("pubDate") or "").strip(),
                })
    except Exception as e:
        print(f"Warning: {name} feed failed: {e}", file=sys.stderr)
    return articles

def fetch_news():
    all_articles = []
    for name, url in RSS_FEEDS:
        all_articles.extend(fetch_rss(name, url))

    seen, unique = set(), []
    for a in all_articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)

    print(json.dumps({
        "source": "RSS Feeds",
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "article_count": len(unique),
        "articles": unique[:20],
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    fetch_news()
