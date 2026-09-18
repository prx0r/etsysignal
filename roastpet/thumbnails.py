#!/usr/bin/env python3
"""roastpet thumbnails — 3 hero concepts as buildable layout specs.

Usage:
    python -m roastpet.thumbnails output/<slug>/

Concepts (same dog, same card, same product):
  A "Magic card"   — phone over physical card, show erupting out of it.
  B "Comedy first" — huge pet close-up at podium, card foregrounded.
  C "Gift first"   — premium card photography, phone beside showing interview.

Output per concept (listing/thumbs/):
  <letter>_spec.json   — exact zones in a 2000x2000 canvas
  <letter>_mock.png    — compositional mockup (zones + labels, not final art)
  <letter>_thumb.png   — the mock shrunk to 150px Etsy-search size

The test the specs must pass: the pet zone + headline zone stay legible
at 150px. If a concept's joke can't survive the shrink, it loses.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

CANVAS = 2000
THUMB = 150

CONCEPTS = {
    "A": {
        "name": "Magic card",
        "promise": "Phone over physical card; roast stage erupts out of it.",
        "zones": {
            "card":     {"box": [250, 1050, 1050, 1850], "fill": (245, 240, 230), "label": "CARD\nJAMES IS 50.\nBUSTER HAS NOTES."},
            "beam":     {"box": [700, 450, 1300, 1100],  "fill": (255, 220, 120), "label": "GLOW / ERUPTION"},
            "phone":    {"box": [950, 250, 1750, 1450],  "fill": (20, 20, 30),    "label": "PHONE\nLATE-NIGHT SET\nBUSTER AT DESK"},
            "headline": {"box": [250, 1500, 1750, 1700], "fill": (180, 30, 30),   "label": "YOUR PET ROASTS YOU"},
        },
    },
    "B": {
        "name": "Comedy first",
        "promise": "Huge pet close-up at podium, physical card foregrounded.",
        "zones": {
            "pet":      {"box": [200, 150, 1800, 1250],  "fill": (150, 100, 60),  "label": "BUSTER HUGE\nBEHIND DESK"},
            "podium":   {"box": [200, 1000, 1800, 1300], "fill": (90, 50, 30),    "label": "PODIUM + MIC"},
            "card":     {"box": [1150, 1300, 1800, 1850],"fill": (245, 240, 230), "label": "CARD\nJAMES IS 50."},
            "headline": {"box": [200, 1350, 1100, 1600], "fill": (180, 30, 30),   "label": "YOUR PET ROASTS YOU"},
        },
    },
    "C": {
        "name": "Gift first",
        "promise": "Premium card photography, phone beside showing interview.",
        "zones": {
            "card":     {"box": [250, 300, 1150, 1500],  "fill": (245, 240, 230), "label": "CARD 3/4 ANGLE\n+ ENVELOPE\nJAMES IS 50."},
            "phone":    {"box": [1200, 500, 1750, 1400], "fill": (20, 20, 30),    "label": "PHONE\nHOST: So, Buster,\ntell us..."},
            "headline": {"box": [250, 1550, 1750, 1750], "fill": (180, 30, 30),   "label": "YOUR PET ROASTS YOU"},
        },
    },
}


def render_mock(concept: dict) -> Image.Image:
    img = Image.new("RGB", (CANVAS, CANVAS), (235, 230, 220))
    d = ImageDraw.Draw(img)
    for key, z in concept["zones"].items():
        x0, y0, x1, y1 = z["box"]
        d.rectangle([x0, y0, x1, y1], fill=z["fill"], outline=(40, 40, 40), width=8)
        d.text((x0 + 30, y0 + 30), f"[{key}]\n{z['label']}", fill=(20, 20, 20))
    return img


def build_thumbs(bundle_dir: str) -> dict:
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    slug = manifest["slug"]
    tdir = bdir / "listing" / "thumbs"
    tdir.mkdir(parents=True, exist_ok=True)

    out = {}
    for letter, concept in CONCEPTS.items():
        spec = {"concept": letter, "name": concept["name"],
                "promise": concept["promise"], "canvas": CANVAS,
                "zones": {k: v["box"] for k, v in concept["zones"].items()},
                "rules": ["1500-2000px square master", "pet enormous",
                          "card print carries the joke, no marketing overlay",
                          "no AI iconography, no gradients",
                          "must read at 150px Etsy-search size"]}
        (tdir / f"{letter}_spec.json").write_text(json.dumps(spec, indent=2))
        mock = render_mock(concept)
        mock.save(tdir / f"{letter}_mock.png")
        mock.resize((THUMB, THUMB), Image.LANCZOS).save(tdir / f"{letter}_thumb.png")
        out[letter] = concept["name"]
        print(f"  {letter} \"{concept['name']}\" → {letter}_mock.png + {letter}_thumb.png")

    print(f"=== THUMBS: {slug} ===")
    print(f"  Files: {tdir}/")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.thumbnails output/<slug>/")
        sys.exit(1)
    build_thumbs(sys.argv[1])
