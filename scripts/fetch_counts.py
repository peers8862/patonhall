#!/usr/bin/env python3
"""Fetch subscriber and member counts from Kit and write counts.json.

Run by .github/workflows/counts.yml on a schedule. Reads the API key from the
KIT_API_SECRET environment variable, which comes from a GitHub Actions secret
and is never stored in this repository.

Two numbers:
  subscribers — everyone on the list
  members     — subscribers carrying the "member" tag, applied by hand in Kit

Design rules:
  - Never write a worse number than we already have because of a transient
    API failure. If a fetch fails, the existing counts.json is left alone and
    the script exits non-zero.
  - The "member" tag not existing yet is not an error. It just means zero.

Standard library only, so the workflow needs no pip install.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent.parent / "counts.json"
MEMBER_TAG = "member"
TIMEOUT = 30


def get(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode())


# --- v3 -------------------------------------------------------------------
# v3 returns total_subscribers / total_subscriptions directly, which is
# exactly what we want and avoids paginating.

V3 = "https://api.convertkit.com/v3"


def v3_subscribers(key: str) -> int:
    q = urllib.parse.urlencode({"api_secret": key, "per_page": 1})
    return int(get(f"{V3}/subscribers?{q}")["total_subscribers"])


def v3_member_count(key: str) -> int:
    q = urllib.parse.urlencode({"api_secret": key})
    tags = get(f"{V3}/tags?{q}").get("tags", [])
    match = next(
        (t for t in tags if str(t.get("name", "")).strip().lower() == MEMBER_TAG),
        None,
    )
    if match is None:
        print(f"  note: no tag named '{MEMBER_TAG}' yet — members = 0")
        return 0
    q = urllib.parse.urlencode({"api_secret": key})
    data = get(f"{V3}/tags/{match['id']}/subscriptions?{q}")
    return int(data["total_subscriptions"])


# --- v4 -------------------------------------------------------------------
# Fallback. Counts come from pagination metadata rather than a total field.

V4 = "https://api.kit.com/v4"


def v4_headers(key: str) -> dict:
    return {"X-Kit-Api-Key": key, "Accept": "application/json"}


def v4_count(url: str, key: str) -> int:
    data = get(url, v4_headers(key))
    for k in ("total_count", "total_subscribers", "total_subscriptions"):
        if k in data:
            return int(data[k])
    pag = data.get("pagination") or {}
    for k in ("total_count", "total"):
        if k in pag:
            return int(pag[k])
    # Last resort: count what came back.
    for k in ("subscribers", "subscriptions"):
        if isinstance(data.get(k), list):
            return len(data[k])
    raise KeyError(f"no count field in response from {url}: {list(data)[:8]}")


def v4_subscribers(key: str) -> int:
    return v4_count(f"{V4}/subscribers?per_page=1", key)


def v4_member_count(key: str) -> int:
    tags = get(f"{V4}/tags?per_page=100", v4_headers(key)).get("tags", [])
    match = next(
        (t for t in tags if str(t.get("name", "")).strip().lower() == MEMBER_TAG),
        None,
    )
    if match is None:
        print(f"  note: no tag named '{MEMBER_TAG}' yet — members = 0")
        return 0
    return v4_count(f"{V4}/tags/{match['id']}/subscribers?per_page=1", key)


def main() -> int:
    key = os.environ.get("KIT_API_SECRET", "").strip()
    if not key:
        print("KIT_API_SECRET is empty or unset", file=sys.stderr)
        return 2

    for label, subs_fn, mem_fn in (
        ("v3", v3_subscribers, v3_member_count),
        ("v4", v4_subscribers, v4_member_count),
    ):
        try:
            subscribers = subs_fn(key)
            members = mem_fn(key)
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError,
                ValueError, TypeError) as e:
            print(f"  {label} failed: {type(e).__name__}: {e}")
            continue

        print(f"  {label} ok — subscribers={subscribers} members={members}")

        previous = {}
        if OUT.exists():
            try:
                previous = json.loads(OUT.read_text())
            except ValueError:
                pass

        # Guard against an API hiccup reporting zero for a list we know is
        # bigger. Zero is only believable if we have never seen more.
        if subscribers == 0 and previous.get("subscribers", 0) > 0:
            print("  refusing to overwrite a positive count with zero")
            return 1

        payload = {"subscribers": subscribers, "members": members, "source": label}
        OUT.write_text(json.dumps(payload, indent=2) + "\n")
        print(f"  wrote {OUT.name}: {payload}")
        return 0

    print("both v3 and v4 failed — leaving counts.json untouched", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
