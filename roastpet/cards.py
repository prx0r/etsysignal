#!/usr/bin/env python3
"""roastpet cards — Card production files from a built bundle.

Usage:
    python -m roastpet.cards output/<slug>/

Reads pipeline_manifest.json, writes card/ production directory:
  front.txt / inside_left.txt / inside_right.txt / back.txt
  qr_payload.txt
  prodigi_layout.json  (Fine Art 5x7, API v4 named print areas)
  front_photo.*        (front_face role photo, copied from bundle photos)

Copy model follows roastpet_checkpoint1_demo/05_card/ fixture.
"""
import json
import shutil
import sys
from pathlib import Path


FINE_ART_5x7 = {
    "provider": "Prodigi",
    "product": "fine_art_greetings_card",
    "size": "5x7 folded",
    "stock": "324gsm, HP Indigo",
    "fulfilment": "UK/EU, worldwide shipping",
    # API v4 named print areas — one asset per surface, no composite file.
    "print_areas": ["front", "inside_left", "inside_right", "back"],
    "artwork_note": "Use the current official Prodigi template/bleed file at order time.",
}


def headline_for(order: dict) -> tuple[str, str]:
    """Front headline + subheadline in the checkpoint fixture voice."""
    pet = order.get("pet_name", "Buster").upper()
    recipient = order.get("recipient_name", "James").upper()
    age = order.get("recipient_age")
    occasion = order.get("occasion", "birthday")
    if age:
        return f"{recipient} IS {age}.", f"{pet} HAS NOTES."
    return f"HAPPY {occasion.upper()} FROM", "SOMEONE WITH STANDARDS"


def build_card(bundle_dir: str) -> dict:
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    order = manifest["order"]
    slug = manifest["slug"]
    beats = manifest["beats"]

    pet = order.get("pet_name", "Buster")
    signoff = order.get("signoff", f"Happy birthday. Love {pet}.")
    roast_lines = [b["text"] for b in beats if b["type"] == "punchline"]
    teaser = roast_lines[0] if roast_lines else ""

    headline, subheadline = headline_for(order)
    qr_url = f"https://roast.pet/{slug}"

    card_dir = bdir / "card"
    card_dir.mkdir(exist_ok=True)

    (card_dir / "front.txt").write_text(
        f"{headline}\n{subheadline}\nA birthday roast from the dog who knows too much.\n")
    (card_dir / "inside_left.txt").write_text(f"{teaser}\n")
    (card_dir / "inside_right.txt").write_text(
        f"{signoff}\n\n{pet.upper()}'S NOT FINISHED.\n[QR]\nScan to watch the roast.\n")
    (card_dir / "back.txt").write_text("Made alive by roast.pet\n")
    (card_dir / "qr_payload.txt").write_text(qr_url + "\n")

    # Front photo: prefer bundle photos, first file wins (intake roles
    # pick front_face when the checkpoint pack is the source).
    photos = sorted((bdir / "photos").glob("*")) if (bdir / "photos").exists() else []
    front_photo = None
    if photos:
        front_photo = photos[0].name
        shutil.copy(photos[0], card_dir / f"front_photo{photos[0].suffix}")

    layout = {
        **FINE_ART_5x7,
        "template_id": "comedy-club-roast-v1",
        "slug": slug,
        "qr_url": qr_url,
        "front": {"headline": headline, "subheadline": subheadline,
                  "photo": front_photo,
                  "note": "Huge pet face. One readable joke. No marketing overlay."},
        "inside_left": {"copy": teaser, "purpose": "teaser / anticipation"},
        "inside_right": {"signoff": signoff, "qr_label": f"{pet.upper()}'S NOT FINISHED.",
                         "cta": "Scan to watch the roast."},
        "back": {"brand": "Made alive by roast.pet"},
    }
    (card_dir / "prodigi_layout.json").write_text(json.dumps(layout, indent=2))

    print(f"=== CARD: {slug} ===")
    print(f"  FRONT: {headline} / {subheadline}")
    print(f"  TEASER: {teaser[:80]}...")
    print(f"  QR: {qr_url}")
    print(f"  PHOTO: {front_photo}")
    print(f"  Files: {card_dir}/")
    return layout


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.cards output/<slug>/")
        sys.exit(1)
    build_card(sys.argv[1])
