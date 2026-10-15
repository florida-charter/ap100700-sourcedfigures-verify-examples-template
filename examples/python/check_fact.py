"""Call check_fact on the Free tier. The caller supplies the official record."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def check_fact(base_url: str, api_key: str, arguments: dict[str, object]) -> dict[str, object]:
    """POST tools/call check_fact. Raises RuntimeError when the host rejects the call."""
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "check_fact", "arguments": arguments},
        }
    ).encode()
    request = urllib.request.Request(
        base_url.rstrip("/") + "/mcp",
        data=body,
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    result = payload["result"]
    if result.get("isError"):
        text = result["content"][0]["text"]
        raise RuntimeError(str(text))
    structured = result["structuredContent"]
    if not isinstance(structured, dict):
        raise RuntimeError("structuredContent")
    return structured


def main() -> int:
    base = os.environ["VERIFY_BASE_URL"]
    key = os.environ["VERIFY_API_KEY"]
    path = os.environ.get("VERIFY_FACTS_FILE", "verify-facts.json")
    facts = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(facts, list) or not facts:
        print("facts file is empty", file=sys.stderr)
        return 1
    failed = 0
    for fact in facts:
        if not isinstance(fact, dict):
            print("fact must be an object", file=sys.stderr)
            return 1
        try:
            record = check_fact(base, key, fact)
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return 1
        verdict = str(record.get("verdict", ""))
        period = str(fact.get("claim_period", ""))
        value = str(fact.get("claim_value", ""))
        print(f"{period} {value} {verdict}".strip())
        if verdict != "matches":
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
