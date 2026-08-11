#!/usr/bin/env python3
"""Fetch subscriber and member counts from Kit and write counts.json.

Run by .github/workflows/counts.yml on a schedule. Credentials come from
GitHub Actions secrets and are never stored in this repository:

  KIT_API_SECRET  required — Kit v3 API Secret (the hidden one in Kit)
  KIT_API_KEY     optional — Kit v3 API Key; v3 needs it to list tags

Either value is also tried against the v4 API, which uses a single key.

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
import re
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
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        # Say which call failed and why. A 401 here almost always means the
        # wrong Kit credential: v3 reads need the API *Secret*, v3 tag listing
        # needs the API *Key*, and v4 needs a v4 key.
        safe = re.sub(r"(api_secret|api_key)=[^&]*", r"\1=***", url)
        raise urllib.error.HTTPError(
            e.url, e.code, f"{e.reason} on {safe}", e.headers, None
        ) from None


# --- v3 -------------------------------------------------------------------
# v3 returns total_subscribers / total_subscriptions directly, which is
# exactly what we want and avoids paginating.

V3 = "https://api.convertkit.com/v3"


def v3_subscribers(key: str) -> int:
    q = urllib.parse.urlencode({"api_secret": key, "per_page": 1})
    return int(get(f"{V3}/subscribers?{q}")["total_subscribers"])


def v3_member_count(secret: str, api_key: str) -> int:
    # Kit v3 splits credentials: listing tags wants the API *Key*, while
    # reading a tag's subscriptions wants the API *Secret*.
    q = urllib.parse.urlencode({"api_key": api_key or secret})
    tags = get(f"{V3}/tags?{q}").get("tags", [])
    match = next(
        (t for t in tags if str(t.get("name", "")).strip().lower() == MEMBER_TAG),
        None,
    )
    if match is None:
        print(f"  note: no tag named '{MEMBER_TAG}' yet — members = 0")
        return 0
    q = urllib.parse.urlencode({"api_secret": secret})
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
    # Kit has three credentials and they are not interchangeable:
    #   KIT_API_SECRET  v3 secret — reads subscriber and tag-subscription data
    #   KIT_API_KEY     v3 key    — lists tags; safe to expose, used in forms
    #   either          v4 key    — one credential for everything, newer API
    secret = os.environ.get("KIT_API_SECRET", "").strip()
    api_key = os.environ.get("KIT_API_KEY", "").strip()

    if not (secret or api_key):
        print("Set KIT_API_SECRET (and ideally KIT_API_KEY too)", file=sys.stderr)
        return 2

    attempts: list[tuple[str, object]] = []
    if secret:
        attempts.append(
            ("v3", lambda: (v3_subscribers(secret),
                            v3_member_count(secret, api_key)))
        )
    for cred, name in ((secret, "secret"), (api_key, "key")):
        if cred:
            attempts.append(
                (f"v4 ({name})",
                 lambda c=cred: (v4_subscribers(c), v4_member_count(c)))
            )

    for label, run in attempts:
        try:
            subscribers, members = run()
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

    print("all credential/API combinations failed — counts.json untouched",
          file=sys.stderr)
    print("  In Kit: Settings -> Advanced -> API. The *Secret* is the hidden one.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
