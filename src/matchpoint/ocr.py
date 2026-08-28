"""OCR layer. Runs Mistral OCR (mistral-ocr-latest) on invoice PNGs and caches
the raw markdown output to data/invoices/ocr_cache/.

The cache is committed to the repo, so the evaluation is reproducible without
a Mistral key. Pass --live to re-OCR from scratch (requires MISTRAL_API_KEY).
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time

import requests

from .config import INVOICE_PNG, OCR_CACHE, DATA, load_env


def ocr_image(png_path) -> str:
    b64 = base64.b64encode(png_path.read_bytes()).decode()
    r = requests.post(
        "https://api.mistral.ai/v1/ocr",
        headers={"Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}",
                 "Content-Type": "application/json"},
        json={"model": "mistral-ocr-latest",
              "document": {"type": "image_url",
                           "image_url": f"data:image/png;base64,{b64}"}},
        timeout=120,
    )
    r.raise_for_status()
    pages = r.json()["pages"]
    return "\n\n".join(p["markdown"] for p in pages)


def get_ocr_text(invoice_id: str) -> str:
    """Read cached OCR text for an invoice id (as used by all pipelines)."""
    safe = invoice_id.replace("/", "_").replace("#", "n")
    f = OCR_CACHE / f"{safe}.md"
    if not f.exists():
        raise FileNotFoundError(
            f"No OCR cache for {invoice_id}. Run: python -m matchpoint.ocr --live")
    return f.read_text()


def main(live: bool) -> None:
    load_env()
    OCR_CACHE.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((DATA / "invoices" / "manifest.json").read_text())
    done = 0
    for entry in manifest:
        safe = entry["invoice_id"].replace("/", "_").replace("#", "n")
        out = OCR_CACHE / f"{safe}.md"
        if out.exists() and not live:
            done += 1
            continue
        png = INVOICE_PNG / f"{safe}.png"
        text = ocr_image(png)
        out.write_text(text)
        done += 1
        print(f"[{done}/{len(manifest)}] OCR {entry['invoice_id']} -> {out.name} ({len(text)} chars)")
        time.sleep(0.4)  # be polite to the API
    print(f"OCR cache complete: {done}/{len(manifest)} invoices.")


if __name__ == "__main__":
    main(live="--live" in sys.argv)
