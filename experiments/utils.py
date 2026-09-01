"""
Shared utilities for CrossLangSQL pipeline scripts.
Centralises helpers that were previously duplicated across dataset folders.
"""

import ast
import json
import os
import re
import socket
import sqlite3
import threading
from typing import Any, Dict, List, Optional

import requests


# ---------------------------------------------------------------------------
# JSON I/O
# ---------------------------------------------------------------------------

def load_json(path: str) -> Any:
    """Load JSON with optional ``//`` line-comment stripping (safe for all datasets)."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    raw = re.sub(r"^\s*//.*$", "", raw, flags=re.MULTILINE)
    return json.loads(raw)


def save_json(data: Any, path: str, indent: int = 2) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


# ---------------------------------------------------------------------------
# LLM client
# ---------------------------------------------------------------------------

# Params that the HKUST-GZ endpoint accepts straight from the OpenAI-style
# ``chat.completions.create(...)`` kwargs. ``extra_body`` is unpacked
# separately so callers like ``qwen_thinking_kwargs`` keep working.
_HKUSTGZ_PASSTHROUGH_PARAMS = (
    "temperature", "max_tokens", "top_p", "stop",
    "presence_penalty", "frequency_penalty", "n", "stream",
    "seed", "response_format", "tools", "tool_choice",
)

def _uses_max_completion_tokens(model: Optional[str]) -> bool:
    """True if *model* expects ``max_completion_tokens`` over ``max_tokens``.

    Newer OpenAI models (the GPT-5 family and o1/o3/o4 reasoning models)
    dropped ``max_tokens`` in favour of ``max_completion_tokens``.
    """
    if not model:
        return False
    name = model.lower()
    return name.startswith(("gpt-5", "o1", "o3", "o4"))


def _supports_custom_temperature(model: Optional[str]) -> bool:
    """False if *model* only accepts the default ``temperature`` (1).

    The same newer OpenAI models (GPT-5 family and o1/o3/o4 reasoning
    models) reject any ``temperature`` other than the default ``1`` with an
    ``unsupported_value`` error, so the param must be dropped for them.
    """
    if not model:
        return True
    name = model.lower()
    return not name.startswith(("gpt-5", "o1", "o3", "o4"))


_HKUSTGZ_HOST_MAP = {
    "aigc-api.hkust-gz.edu.cn": "10.121.10.250",
    "gpt-api.hkust-gz.edu.cn": "10.121.10.250",
}
_DNS_PATCH_LOCK = threading.Lock()
_DNS_PATCHED = False


def install_internal_dns(host_map: Dict[str, str] = _HKUSTGZ_HOST_MAP) -> None:
    """Resolve selected hostnames directly to fixed intranet IPs.

    Monkey-patches ``socket.getaddrinfo`` once (process-wide) so the
    HKUST-GZ hostnames bypass public DNS and connect straight to the LAN
    IP. The HTTP Host header and TLS SNI still use the original hostname,
    so certificate verification keeps working.

    Idempotent and thread-safe: a one-time global patch avoids the
    per-request lock that previously serialized every HKUST-GZ call.
    """
    global _DNS_PATCHED
    with _DNS_PATCH_LOCK:
        if _DNS_PATCHED:
            return
        normalized = {host.lower(): ip for host, ip in host_map.items()}
        original_getaddrinfo = socket.getaddrinfo

        def patched_getaddrinfo(host, *args, **kwargs):
            mapped_host = normalized.get(str(host).lower(), host)
            return original_getaddrinfo(mapped_host, *args, **kwargs)

        socket.getaddrinfo = patched_getaddrinfo
        _DNS_PATCHED = True


class _Message:
    __slots__ = ("role", "content")

    def __init__(self, content: str, role: str = "assistant"):
        self.role = role
        self.content = content


class _Choice:
    __slots__ = ("index", "message", "finish_reason")

    def __init__(self, content: str, index: int = 0, finish_reason: str = "stop"):
        self.index = index
        self.message = _Message(content)
        self.finish_reason = finish_reason


class _ChatCompletion:
    """Minimal stand-in for ``openai.types.ChatCompletion``."""

    def __init__(self, content: str, model: str = "", raw: Optional[dict] = None):
        self.choices = [_Choice(content)]
        self.model = model
        self._raw = raw  # for debugging


class _Model:
    __slots__ = ("id", "_raw")

    def __init__(self, model_id: str, raw: Optional[dict] = None):
        self.id = model_id
        self._raw = raw or {"id": model_id}

    def model_dump(self) -> dict:
        return self._raw


class _ModelList:
    """Minimal stand-in for ``openai.types.SyncPage[Model]``."""

    def __init__(self, data: List[_Model]):
        self.data = data


class _ModelsNamespace:
    def __init__(self, client: "HKUSTGZClient"):
        self._client = client

    def list(self) -> _ModelList:
        return self._client._list_models()


class _ChatCompletionsNamespace:
    def __init__(self, client: "HKUSTGZClient"):
        self._client = client

    def create(self, **kwargs) -> _ChatCompletion:
        return self._client._create_chat_completion(**kwargs)


class _ChatNamespace:
    def __init__(self, client: "HKUSTGZClient"):
        self.completions = _ChatCompletionsNamespace(client)


class HKUSTGZClient:
    """OpenAI-compatible adapter for the HKUST-GZ AIGC API.

    The HKUST-GZ endpoint exposes the *full* chat-completions URL
    (e.g. ``https://aigc-api.hkust-gz.edu.cn/v1/chat/completions``) rather
    than an OpenAI-style base URL, so the official ``openai`` SDK can't
    be pointed at it directly without producing a doubled
    ``/chat/completions`` path.

    This thin adapter mirrors the
    ``client.chat.completions.create(model=..., messages=...)`` surface
    used everywhere in the codebase, so callers don't need to special-case
    HKUST-GZ.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: Optional[float] = 600.0,
    ):
        if not api_key:
            raise RuntimeError("HKUSTGZClient requires an api_key")
        if not base_url:
            raise RuntimeError("HKUSTGZClient requires a base_url")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.chat = _ChatNamespace(self)
        self.models = _ModelsNamespace(self)
        install_internal_dns()

    def _models_url(self) -> str:
        return self.base_url.removesuffix("/chat/completions") + "/models"

    def _list_models(self) -> _ModelList:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(
            self._models_url(),
            headers=headers,
            timeout=self.timeout,
        )
        if resp.status_code >= 400:
            raise RuntimeError(
                f"HKUSTGZ API error {resp.status_code}: {resp.text[:500]}"
            )
        try:
            result = resp.json()
        except ValueError as e:
            raise RuntimeError(
                f"HKUSTGZ API returned non-JSON response: {resp.text[:500]}"
            ) from e
        if isinstance(result, dict) and "code" in result and "data" not in result:
            # The HKUST-GZ gateway accepts chat completions but returns an
            # in-body ``code: 401`` for ``GET /models`` (HTTP status is 200).
            # Model listing simply isn't exposed, so surface that clearly
            # instead of a misleading "Unauthorized".
            raise RuntimeError(
                "HKUST-GZ endpoint does not support model listing "
                f"(/models returned code {result.get('code')}: "
                f"{result.get('msg', result)})"
            )

        raw_models = result.get("data") if isinstance(result, dict) else result
        if not isinstance(raw_models, list):
            raise RuntimeError(
                f"HKUSTGZ API unexpected models response shape: {result}"
            )
        models: List[_Model] = []
        for item in raw_models:
            if isinstance(item, dict):
                model_id = item.get("id") or item.get("model")
                if model_id:
                    models.append(_Model(str(model_id), raw=item))
            elif item:
                models.append(_Model(str(item)))
        return _ModelList(models)

    def _create_chat_completion(self, **kwargs) -> _ChatCompletion:
        model = kwargs.pop("model", None)
        messages = kwargs.pop("messages", None)
        if not model:
            raise ValueError("HKUSTGZClient: 'model' is required")
        if not messages:
            raise ValueError("HKUSTGZClient: 'messages' is required")

        payload: Dict[str, Any] = {"model": model, "messages": messages}
        uses_max_completion_tokens = _uses_max_completion_tokens(model)
        supports_custom_temperature = _supports_custom_temperature(model)
        for k in _HKUSTGZ_PASSTHROUGH_PARAMS:
            if k in kwargs and kwargs[k] is not None:
                # Newer OpenAI models (e.g. gpt-5*) reject ``max_tokens`` and
                # require ``max_completion_tokens`` instead. Map transparently
                # so callers can keep passing ``max_tokens``.
                if k == "max_tokens" and uses_max_completion_tokens:
                    payload["max_completion_tokens"] = kwargs[k]
                elif k == "temperature" and not supports_custom_temperature:
                    # These models only accept the default temperature (1);
                    # drop any other value to avoid an ``unsupported_value`` error.
                    continue
                else:
                    payload[k] = kwargs[k]
        # ``extra_body`` mirrors OpenAI SDK semantics: vendor-specific
        # fields (e.g. Qwen's ``enable_thinking``) are merged into the
        # top-level JSON body.
        extra_body = kwargs.pop("extra_body", None) or {}
        for k, v in extra_body.items():
            payload[k] = v

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        resp = requests.post(
            self.base_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=self.timeout,
        )
        if resp.status_code >= 400:
            raise RuntimeError(
                f"HKUSTGZ API error {resp.status_code}: {resp.text[:500]}"
            )
        try:
            result = resp.json()
        except ValueError as e:
            raise RuntimeError(
                f"HKUSTGZ API returned non-JSON response: {resp.text[:500]}"
            ) from e
        if isinstance(result, dict) and "code" in result and "choices" not in result:
            raise RuntimeError(
                f"HKUSTGZ API error {result.get('code')}: {result.get('msg', result)}"
            )
        try:
            content = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(
                f"HKUSTGZ API unexpected response shape: {result}"
            ) from e
        return _ChatCompletion(content=content or "", model=model, raw=result)


def _is_hkustgz_url(url: Optional[str]) -> bool:
    """True if *url* looks like a full chat-completions endpoint.

    OpenAI-style base URLs stop at the API version segment (``.../v1``)
    and let the SDK append ``/chat/completions`` itself. HKUST-GZ instead
    publishes the full ``.../v1/chat/completions`` URL, so any URL ending
    with that suffix is routed through the request-based adapter.
    """
    if not url:
        return False
    return url.rstrip("/").endswith("/chat/completions")


def get_llm_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
):
    """Create an OpenAI-compatible LLM client from env / explicit args.

    Env vars checked: ``OPENAI_API_KEY``, ``OPENAI_BASE_URL``.

    If ``base_url`` looks like a full chat-completions URL
    (e.g. the HKUST-GZ AIGC endpoint), a ``requests``-based adapter
    (``HKUSTGZClient``) is returned. It exposes the same
    ``chat.completions.create(...)`` surface so every caller in the
    codebase works unchanged.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    url = base_url or os.environ.get("OPENAI_BASE_URL")
    if not key:
        raise RuntimeError(
            "No API key. Set OPENAI_API_KEY or pass --api_key."
        )
    if _is_hkustgz_url(url):
        return HKUSTGZClient(api_key=key, base_url=url)

    from openai import OpenAI
    return OpenAI(api_key=key, base_url=url)


# ---------------------------------------------------------------------------
# vLLM client (local endpoint reached through the SSH tunnel)
# ---------------------------------------------------------------------------

# Defaults mirror script/vllm/call_model.{sh,py}: the model is served by vLLM
# and reached at http://localhost:18001/v1 via the SSH tunnel. vLLM is
# OpenAI-compatible and ignores the API key, but the SDK still requires a
# non-empty string.
VLLM_DEFAULT_BASE_URL = "http://localhost:18001/v1"
VLLM_DEFAULT_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"
VLLM_DEFAULT_API_KEY = "EMPTY"


def get_vllm_client(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
):
    """Return an OpenAI-compatible client for the local vLLM endpoint.

    Thin convenience wrapper around the official ``openai`` SDK pointed at
    the vLLM server (see ``script/vllm/call_model.py``). vLLM does not check
    the API key, so it falls back to a placeholder when none is given.

    Env vars checked (in order, when the matching arg is omitted):
      * base_url -> ``VLLM_BASE_URL`` -> ``VLLM_DEFAULT_BASE_URL``
      * api_key  -> ``VLLM_API_KEY``  -> ``VLLM_DEFAULT_API_KEY``
    """
    url = base_url or os.environ.get("VLLM_BASE_URL") or VLLM_DEFAULT_BASE_URL
    key = api_key or os.environ.get("VLLM_API_KEY") or VLLM_DEFAULT_API_KEY

    from openai import OpenAI
    return OpenAI(api_key=key, base_url=url)


def qwen_thinking_kwargs(model: Optional[str]) -> Dict[str, Any]:
    """Extra kwargs needed by DashScope's Qwen3 OpenAI-compatible endpoint.

    Qwen3 / Qwen3-VL / Qwen3-MOE chat models reject non-streaming calls
    unless ``enable_thinking`` is explicitly set to ``false``::

        Error code: 400 - parameter.enable_thinking must be set to false
        for non-streaming calls

    Returns ``{"extra_body": {"enable_thinking": False}}`` for those models
    and ``{}`` otherwise, so callers can splat the result with ``**``.
    """
    if not model:
        return {}
    name = model.strip().lower()
    if name.startswith("qwen3"):
        return {"extra_body": {"enable_thinking": False}}
    return {}


def hkustgz_request_call(url: str, key: str, model: str, content: str) -> str:
    """One-shot text-in/text-out helper for the HKUST-GZ AIGC endpoint.

    Thin wrapper around :class:`HKUSTGZClient` for callers that just want
    the response text. Prefer :func:`get_llm_client` for new code so the
    same call site works with both OpenAI-compatible and HKUST-GZ
    endpoints.
    """
    client = HKUSTGZClient(api_key=key, base_url=url)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
        )
    except Exception as e:
        print(e)
        return str(e)
    return resp.choices[0].message.content


# ---------------------------------------------------------------------------
# SQLite helpers
# ---------------------------------------------------------------------------

def execute_query(
    db_path: str,
    query: str,
    encoding: str = "utf-8",
    timeout: Optional[float] = 10,
):
    """Execute *query* and return sorted rows, or an error string.

    Uses a background thread so a hard ``timeout`` (seconds) can be enforced.
    """
    result: list = [None]

    def _run():
        try:
            conn = sqlite3.connect(db_path)
            conn.text_factory = lambda b: b.decode(encoding, errors="replace")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()
            result[0] = sorted(
                [tuple(r) for r in rows], key=lambda x: str(x)
            )
        except Exception as e:
            result[0] = f"Error: {e}"

    if timeout is None or timeout <= 0:
        _run()
        return result[0]

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout=timeout)
    if t.is_alive():
        return "Error: timeout"
    return result[0]


def is_system_table(table_name: str) -> bool:
    return (table_name or "").lower().startswith("sqlite_")


# ---------------------------------------------------------------------------
# LLM JSON parsing
# ---------------------------------------------------------------------------

def parse_llm_json(content: str, context_info: str = "") -> Optional[dict]:
    """Clean and parse a JSON object from an LLM response string.

    Handles markdown code-fences, trailing text after the last ``}``,
    and falls back to ``ast.literal_eval``.
    """
    if not content:
        return None
    clean = re.sub(r"```json\s*|\s*```", "", content).strip()
    last_brace = clean.rfind("}")
    if last_brace != -1:
        clean = clean[: last_brace + 1]
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass
    try:
        return ast.literal_eval(clean)
    except Exception:
        if context_info:
            print(f"[Warning] Could not parse LLM JSON for {context_info}")
            print(f"Content: {content}")
        return None
