#!/usr/bin/env python3
"""roastpet cards — Card production files from a built bundle.

Usage:
    python -m roastpet.cards output/<slug>/

Reads pipeline_manifest.json, writes card/ production directory:
  front.txt / inside_left.txt / inside_right.txt / back.txt
  qr_payload.txt
  prodigi_layout.json  (Fine Art 5x7, API v4 named print areas)
  front_photo.*        (front_face role photo, copied from bundle photos)

Copy model follows northstar.md (V1 card).
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


def build_card(bundle_dir: str) -> dict:
    """Build V1 card production files (northstar.md).

    Front: podium portrait + killer card_line (ONE line, not the roast).
    Inside left: TONIGHT'S ROASTER.
    Inside right: "has more to say" + QR + WATCH YOUR ROAST + message.
    Back: tiny roast.pet mark.
    """
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    order = manifest["order"]
    slug = manifest["slug"]
    roast = manifest.get("roast", {})
    beats = manifest["beats"]

    pet = roast.get("visual", {}).get("pet", "buster").upper()
    pet_title = pet.capitalize()
    signoff = roast.get("signoff") or order.get("signoff", "")
    card_line = roast.get("card_line", "")
    qr_url = f"https://roast.pet/r/{slug}"

    card_dir = bdir / "card"
    card_dir.mkdir(exist_ok=True)

    (card_dir / "front.txt").write_text(
        f"ROAST.PET PRESENTS\n\n{pet_title}\n\n\"{card_line}\"\n\nTHE ROAST\n")
    (card_dir / "inside_left.txt").write_text(f"TONIGHT'S ROASTER: {pet_title}\n")
    (card_dir / "inside_right.txt").write_text(
        f"{pet_title} has more to say.\n\n[QR]\n\nWATCH YOUR ROAST\n\n{signoff}\n")
    (card_dir / "back.txt").write_text("roast.pet\n")
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
        "template_id": "roast-v1-podium",
        "slug": slug,
        "qr_url": qr_url,
        "front": {"brand": "ROAST.PET PRESENTS", "pet": pet_title,
                  "card_line": card_line, "footer": "THE ROAST",
                  "photo": front_photo,
                  "note": "Pet at podium, one killer line. No marketing overlay."},
        "inside_left": {"copy": f"TONIGHT'S ROASTER: {pet_title}"},
        "inside_right": {"teaser": f"{pet_title} has more to say.",
                         "qr_label": "WATCH YOUR ROAST", "message": signoff},
        "back": {"brand": "roast.pet"},
    }
    (card_dir / "prodigi_layout.json").write_text(json.dumps(layout, indent=2))

    print(f"=== CARD: {slug} ===")
    print(f"  FRONT: ROAST.PET PRESENTS / {pet_title} / \"{card_line}\"")
    print(f"  QR: {qr_url}")
    print(f"  PHOTO: {front_photo}")
    print(f"  Files: {card_dir}/")
    return layout


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.cards output/<slug>/")
        sys.exit(1)
    build_card(sys.argv[1])
