#!/usr/bin/env python3
"""roastpet video — 15s silent listing video storyboard from a bundle.

Usage:
    python -m roastpet.video output/<slug>/

Etsy strips audio from listing videos and caps them at 3-15s, so the
storyboard is visual-transformation + giant subtitles only. Matches the
CardReveal composition in roast-pet-listing (450 frames @ 30fps).
"""
import json
import sys
from pathlib import Path


def build_storyboard(bundle_dir: str) -> str:
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    order = manifest["order"]
    beats = manifest["beats"]

    pet = order.get("pet_name", "Buster")
    recipient = order.get("recipient_name", "James")
    punchlines = [b["text"] for b in beats if b["type"] == "punchline"]
    full_roast = punchlines[0] if punchlines else ""
    # Subtitle rule: max 8 words per card. Truncate, never wrap tiny.
    words = full_roast.split()
    roast = " ".join(words[:8]) + ("..." if len(words) > 8 else "")

    md = f"""# Listing video storyboard — {manifest['slug']}

Format: 1920x1080, 450 frames @ 30fps = 15.0s. NO AUDIO TRACK (Etsy strips it).
Render: `npm run render:listing` in roast-pet-listing/ (CardReveal composition).

| Shot | Frames | Time | Visual | Giant subtitle |
|------|--------|------|--------|----------------|
| 1 | 0-60 | 0-2s | Normal dog photo, slow push-in | *(none — let the photo breathe)* |
| 2 | 60-120 | 2-4s | Photo folds/transforms into the printed birthday card | A CARD |
| 3 | 120-180 | 4-6s | Phone slides into frame over the card, scan line sweeps | SCAN IT |
| 4 | 180-300 | 6-10s | Late-night set erupts: {pet} at desk, dog audience mid-eruption | “{roast}” |
| 5 | 300-360 | 10-12s | Rapid second example: shocked Chihuahua cutaway | {recipient.upper()} HAS BEEN ROASTED |
| 6 | 360-450 | 12-15s | Title card on show-set background | YOUR PET. THEIR OWN COMEDY SHOW. |

Subtitle rules: min 96px, white with black drop shadow, max 8 words per card.
No dialogue audio, no voiceover, no music dependency — the video must land muted on autoplay.
"""
    out = bdir / "listing" / "video_storyboard.md"
    out.write_text(md)
    print(f"=== STORYBOARD: {manifest['slug']} ===")
    print(f"  {out}")
    return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.video output/<slug>/")
        sys.exit(1)
    build_storyboard(sys.argv[1])
