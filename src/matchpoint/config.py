"""Project paths and .env loading (no python-dotenv dependency)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
# MATCHPOINT_WORLD=<name> points every pipeline at data/worlds/<name>/ —
# used for the held-out stress batch (seed 43) without touching any code.
_WORLD = os.environ.get("MATCHPOINT_WORLD")
_BASE = (DATA / "worlds" / _WORLD) if _WORLD else DATA
ERP = _BASE / "erp"
INVOICE_PNG = _BASE / "invoices" / "png"
OCR_CACHE = _BASE / "invoices" / "ocr_cache"
GOLD = _BASE / "gold"
MANIFEST = _BASE / "invoices" / "manifest.json"
OUT = ROOT / "out"
TRAJ = ROOT / "trajectories"
RESULTS = ROOT / "eval" / "results"


def load_env() -> None:
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    missing = [k for k in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL") if not os.environ.get(k)]
    if missing:
        raise SystemExit(
            f"Missing env vars: {', '.join(missing)}. Copy .env.example to .env and fill them in."
        )
