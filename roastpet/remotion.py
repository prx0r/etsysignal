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
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    order = manifest["order"]
    beats = manifest["beats"]
    card_dir = bdir / "card"

    front = (card_dir / "front.txt").read_text().splitlines() if (card_dir / "front.txt").exists() else ["", ""]
    punchlines = [b["text"] for b in beats if b["type"] == "punchline"]

    pet = {
        "petName": order.get("pet_name", "Buster"),
        "recipient": order.get("recipient_name", "James"),
        "occasion": order.get("occasion", "birthday"),
        "headline": front[0] if len(front) > 0 else "",
        "subheadline": front[1] if len(front) > 1 else "",
        "punchline": punchlines[0] if punchlines else "",
        "signoff": order.get("signoff", ""),
        "qrUrl": f"https://roast.pet/{manifest['slug']}",
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
