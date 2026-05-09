#!/usr/bin/env python3
"""Fetch market gainers/losers from Yahoo Finance — no API key required."""

import sys
import json
from urllib.request import urlopen, Request
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

def fetch_json(url):
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Warning: {url} failed: {e}", file=sys.stderr)
        return None

def parse_quotes(data):
    if not data:
        return []
    quotes = (
        data.get("finance", {})
            .get("result", [{}])[0]
            .get("quotes", [])
    )
    out = []
    for q in quotes[:10]:
        out.append({
            "ticker": q.get("symbol", ""),
            "change_percent": round(q.get("regularMarketChangePercent", {}).get("raw", 0), 2),
            "price": q.get("regularMarketPrice", {}).get("raw", 0),
            "volume": q.get("regularMarketVolume", {}).get("raw", 0),
            "name": q.get("shortName", ""),
        })
    return out

BASE = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?formatted=true&region=US&lang=en-US&count=10&scrIds="

def fetch_market_data():
    results = {
        "source": "Yahoo Finance",
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "gainers": parse_quotes(fetch_json(BASE + "day_gainers")),
        "losers":  parse_quotes(fetch_json(BASE + "day_losers")),
    }
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    fetch_market_data()
