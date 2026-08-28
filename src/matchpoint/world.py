"""Loads the ERP world and invoice batch used by every pipeline."""
from __future__ import annotations

import json

from .config import ERP, GOLD, MANIFEST


def load_world() -> dict:
    return {
        "vendors": json.loads((ERP / "vendors.json").read_text()),
        "pos": json.loads((ERP / "pos.json").read_text()),
        "grns": json.loads((ERP / "grns.json").read_text()),
        "payments": json.loads((ERP / "payments.json").read_text()),
    }


def load_vendor_memory() -> dict:
    return json.loads((ERP / "vendor_memory.json").read_text())


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST.read_text())


def load_gold() -> dict:
    return json.loads((GOLD / "labels.json").read_text())
