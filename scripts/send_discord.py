#!/usr/bin/env python3
"""Send a report to Discord via webhook, splitting long messages as needed."""

import os
import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import time

DISCORD_MAX_LENGTH = 2000

def split_message(content, max_length=DISCORD_MAX_LENGTH):
    """Split a message into chunks that fit within Discord's character limit.
    Tries to split at section boundaries (double newlines) first, then single newlines."""
    if len(content) <= max_length:
        return [content]

    chunks = []
    remaining = content

    while remaining:
        if len(remaining) <= max_length:
            chunks.append(remaining)
            break

        # Try to split at a section boundary (double newline)
        split_pos = remaining.rfind("\n\n", 0, max_length)
        if split_pos == -1:
            # Try single newline
            split_pos = remaining.rfind("\n", 0, max_length)
        if split_pos == -1:
            # Last resort: split at max_length
            split_pos = max_length

        chunks.append(remaining[:split_pos].rstrip())
        remaining = remaining[split_pos:].lstrip()

    return chunks

def send_to_discord(content):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print(json.dumps({"error": "DISCORD_WEBHOOK_URL environment variable not set"}))
        sys.exit(1)

    chunks = split_message(content)
    sent = 0
    errors = []

    for i, chunk in enumerate(chunks):
        payload = json.dumps({"content": chunk}).encode("utf-8")
        req = Request(
            webhook_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "MarketNewsDigest/1.0",
            },
            method="POST",
        )

        try:
            with urlopen(req, timeout=15) as response:
                sent += 1
                # Respect Discord rate limits
                if i < len(chunks) - 1:
                    time.sleep(0.5)
        except (URLError, HTTPError) as e:
            errors.append(f"Chunk {i+1}: {str(e)}")

    result = {
        "total_chunks": len(chunks),
        "sent": sent,
        "errors": errors if errors else None,
        "status": "success" if sent == len(chunks) else "partial_failure" if sent > 0 else "failure",
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Read from stdin if no argument provided
        content = sys.stdin.read().strip()
    else:
        content = sys.argv[1]

    if not content:
        print(json.dumps({"error": "No content provided. Pass as argument or pipe to stdin."}))
        sys.exit(1)

    send_to_discord(content)
