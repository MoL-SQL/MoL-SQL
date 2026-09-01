"""Deterministic identifiers for release artifacts."""

from __future__ import annotations

from hashlib import sha256


def stable_id(prefix: str, *parts: object, length: int = 20) -> str:
    """Return a stable identifier from typed, ordered string parts."""

    payload = "\0".join(str(part) for part in parts).encode("utf-8")
    return f"{prefix}_{sha256(payload).hexdigest()[:length]}"
