#!/usr/bin/env python3
"""Upload report to GitHub via REST API — no git commands needed."""

import os
import sys
import json
import base64
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import datetime

REPO = "pinkpink6898/MarketNews"

def push_report(content, filename):
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("Error: GH_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    api_url = f"https://api.github.com/repos/{REPO}/contents/reports/{filename}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "MarketNewsDigest/1.0",
    }

    # Get existing file SHA if it exists (required for update)
    sha = None
    try:
        req = Request(api_url, headers=headers)
        with urlopen(req, timeout=15) as resp:
            sha = json.loads(resp.read()).get("sha")
    except HTTPError:
        pass

    # Upload file
    payload = {
        "message": f"report: {filename}",
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": "main",
    }
    if sha:
        payload["sha"] = sha

    req = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="PUT",
    )

    try:
        with urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            html_url = result.get("content", {}).get("html_url", "")
            print(f"Report pushed to GitHub: {html_url}")
    except HTTPError as e:
        body = e.read().decode()
        print(f"GitHub API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    content = sys.stdin.read() if len(sys.argv) < 2 else sys.argv[1]
    date_str = datetime.utcnow().strftime("%Y%m%d")
    filename = f"premarket_{date_str}.txt"
    push_report(content, filename)
