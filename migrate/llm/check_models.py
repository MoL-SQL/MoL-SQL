#!/usr/bin/env python3
"""
List models available at the configured OpenAI-compatible endpoint.

Reads ``OPENAI_BASE_URL`` and ``OPENAI_API_KEY`` from the environment
(override via CLI flags) and prints the model IDs returned by ``GET /models``.

``--api_key`` and ``--base_url`` accept either a literal value or the *name*
of an exported environment variable (e.g. ``MIYUN_CLAUDE_API_KEY``); when the
argument matches a defined env var, its value is used.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_llm_client


def _resolve_env(value: str | None) -> str | None:
    """Return ``os.environ[value]`` if it's a defined env var name, else ``value``."""
    if value is None:
        return None
    resolved = os.environ.get(value)
    return resolved if resolved is not None else value


def list_models(api_key: str | None, base_url: str | None, show_raw: bool) -> int:
    api_key = _resolve_env(api_key)
    base_url = _resolve_env(base_url)
    client = get_llm_client(api_key=api_key, base_url=base_url)

    print(f"[endpoint] {client.base_url}")
    try:
        resp = client.models.list()
    except Exception as e:
        print(f"[error] failed to list models: {e}", file=sys.stderr)
        return 1

    models = sorted(getattr(m, "id", str(m)) for m in resp.data)
    print(f"[count]    {len(models)} model(s)")
    print("-" * 60)
    for mid in models:
        print(mid)

    if show_raw:
        print("-" * 60)
        print("[raw]")
        for m in resp.data:
            print(m.model_dump() if hasattr(m, "model_dump") else m)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List models from an OpenAI-compatible endpoint.",
    )
    parser.add_argument(
        "--api_key",
        default="OPENAI_API_KEY",
        help="API key value, or the name of an exported env var (e.g. OPENAI_API_KEY).",
    )
    parser.add_argument(
        "--base_url",
        default="OPENAI_BASE_URL",
        help="Base URL value, or the name of an exported env var (e.g. OPENAI_BASE_URL).",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Also print the full raw model objects.",
    )
    args = parser.parse_args()

    sys.exit(list_models(args.api_key, args.base_url, args.raw))


if __name__ == "__main__":
    main()
