#!/usr/bin/env python3
"""roastpet remotion — Export pet.json from a built bundle.

Usage:
    python -m roastpet.remotion output/<slug>/

Writes roast-pet-listing/src/pet.json. Change pet.json → re-render
hero, listing video, vertical ad, how-it-works, reroll. One visual engine.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def export(bundle_dir: str) -> dict:
    """Export pet.json from a bundle's roast.json (canonical consumer)."""
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    order = manifest["order"]
    roast = manifest.get("roast", {})
    norder = manifest.get("normalized_order", {})

    pet = {
        "petName": roast.get("visual", {}).get("pet", "buster").capitalize(),
        "recipient": (norder.get("target", {}) or {}).get("name", "James"),
        "occasion": order.get("occasion", "birthday"),
        "headline": roast.get("headline", ""),
        "subheadline": roast.get("card_line", ""),
        "punchline": roast.get("card_line", ""),
        "signoff": roast.get("signoff", ""),
        "qrUrl": f"https://roast.pet/r/{manifest['slug']}",
        "take1Label": "Original",
        "take2Label": manifest.get("style", "Meaner").capitalize(),
    }
    out = REPO_ROOT / "roast-pet-listing" / "src" / "pet.json"
    out.write_text(json.dumps(pet, indent=2))
    print(f"=== PET.JSON: {manifest['slug']} ===")
    print(f"  {out}")
    return pet


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.remotion output/<slug>/")
        sys.exit(1)
    export(sys.argv[1])
