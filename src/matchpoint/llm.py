"""Thin OpenAI-compatible chat client. No SDK dependency — plain HTTPS.

Reads LLM_BASE_URL / LLM_API_KEY / LLM_MODEL from environment (.env is loaded
by config.load_env()). Every call is recorded by the trajectory logger when
one is passed in, so agent runs are fully replayable.
"""
from __future__ import annotations

import json
import os
import time

import requests


class LLMError(RuntimeError):
    pass


def _headers(api_key: str) -> dict:
    # Azure accepts api-key; OpenAI expects Authorization. Send both — each
    # provider ignores the header it doesn't use.
    return {
        "Content-Type": "application/json",
        "api-key": api_key,
        "Authorization": f"Bearer {api_key}",
    }


def chat(
    messages: list[dict],
    tools: list[dict] | None = None,
    tool_choice: str | None = None,
    response_json: bool = False,
    max_tokens: int = 4000,
    retries: int = 3,
    trajectory=None,
    agent: str = "llm",
) -> dict:
    """Returns the assistant message dict. Raises LLMError after retries."""
    base = os.environ["LLM_BASE_URL"].rstrip("/")
    model = os.environ["LLM_MODEL"]
    payload: dict = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    if tools:
        payload["tools"] = tools
        if tool_choice:
            payload["tool_choice"] = tool_choice
    if response_json:
        payload["response_format"] = {"type": "json_object"}

    last_err: Exception | None = None
    for attempt in range(retries):
        t0 = time.time()
        try:
            r = requests.post(
                f"{base}/chat/completions",
                headers=_headers(os.environ["LLM_API_KEY"]),
                json=payload,
                timeout=300,
            )
            if r.status_code == 429:
                wait = min(2 ** (attempt + 2), 30)
                time.sleep(wait)
                last_err = LLMError(f"429 rate limited (attempt {attempt + 1})")
                continue
            r.raise_for_status()
            body = r.json()
            msg = body["choices"][0]["message"]
            usage = body.get("usage", {})
            if trajectory is not None:
                trajectory.log_llm(
                    agent=agent,
                    messages=messages,
                    tools=[t["function"]["name"] for t in tools] if tools else [],
                    response=msg,
                    usage=usage,
                    latency_s=round(time.time() - t0, 2),
                    attempt=attempt + 1,
                )
            return msg
        except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
            last_err = e
            time.sleep(2 ** attempt)
    raise LLMError(f"LLM call failed after {retries} attempts: {last_err}")


def extract_json(text: str) -> dict:
    """Parse JSON from a model reply, tolerating markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object found in: {text[:200]}")
    return json.loads(text[start : end + 1])
