#!/usr/bin/env python3
"""roastpet listing — V1 Etsy listing pack from a built bundle.

Usage:
    python -m roastpet.listing output/<slug>/

V1 (northstar.md): ONE listing = ONE concept (podium roast). Four
personalization fields, 8 images, 2 silent videos. Buyer personalizes
content, never layout.
"""
import json
import sys
from pathlib import Path


TITLE = "Personalized Pet Roast Birthday Card + Video | Watch Your Pet Roast You | Funny Custom Card From Your Dog"

TAGS = [
    "personalized pet roast", "funny dog birthday card", "custom pet video",
    "pet roast card", "funny birthday card for him", "dog dad gift",
    "scan to watch card", "qr birthday card", "pet lover gift",
    "funny 50th birthday", "dog roast video", "personalised pet gift",
    "birthday card from dog",
]

# Exactly four fields. No show-style selector (one listing = one concept).
PERSONALIZATION = {
    "personalization_questions": [
        {
            "question_type": "labeled_upload",
            "question_text": "Pet photos",
            "instructions": "Upload 3-5 clear photos showing your pet's face and body.",
            "required": True,
            "max_allowed_files": 5,
        },
        {
            "question_type": "text_input",
            "question_text": "Who are we roasting?",
            "instructions": "Name + relationship to pet. Example: James, Biscuit's dad.",
            "required": True,
            "max_allowed_characters": 120,
        },
        {
            "question_type": "text_input",
            "question_text": "Give us the dirt",
            "instructions": "Tell us 3-5 funny facts, habits or embarrassing stories about them. You supply facts; your pet supplies comedy.",
            "required": True,
            "max_allowed_characters": 1024,
        },
        {
            "question_type": "dropdown",
            "question_text": "Roast level",
            "required": True,
            "options": [{"label": "Playful"}, {"label": "Spicy"}, {"label": "Savage"}],
        },
    ]
}

# Dropdown label → pipeline intensity.
INTENSITY_MAP = {"Playful": "playful", "Spicy": "spicy", "Savage": "savage"}


def description_for(order: dict) -> str:
    return """PERSONALIZED PET ROAST CARD → SCAN IT → YOUR PET ROASTS YOU.

Your pet, behind a podium, under a spotlight, roasting the birthday legend in your life. Printed on a premium 5x7 card with a QR code that plays the actual roast.

WHAT YOU GET
- Premium 5x7 Fine Art birthday card with your pet's roast portrait + killer headline
- QR code inside the card → private roast video (30-60 seconds)
- 1 FREE reroll — funnier, meaner, gentler, more personal, or a different voice. You keep both takes.

HOW IT WORKS
1. Upload 3-5 photos of your pet
2. Tell us who we're roasting
3. Give us the dirt — 3-5 funny facts or stories
4. Pick the roast level. Your pet does the rest.

YOU GIVE US THE DIRT. YOUR PET DOES THE REST.
Best results: daylight, sharp photos, no filters or stickers. Phone photos are fine.
The card design shown is the design you receive — you personalize the content, not the layout.
"""


def shotlist_for(slug: str, roast: dict) -> str:
    line = roast.get("card_line", "")
    return f"""# Listing images — {slug} (8 images, northstar.md)

1. THUMBNAIL — finished card, 2000x2000+: THE ROAST / pet at podium / "{line}" / envelope / phone corner showing SAME pet on stage. The product explains the joke.
2. MAGIC — YOUR PET ROASTS YOU. Upload pet → Receive card → Scan → Watch roast.
3. SHOW — phone fullscreen: pet at podium, subtitle, dog audience.
4. PERSONALIZATION — the 4 inputs. YOU GIVE US THE DIRT. YOUR PET DOES THE REST.
5. PHYSICAL CARD — front / inside / back. A real printed card arrives.
6. REROLL — Includes one free reroll. Take 1 / Take 2.
7. GIFTING — recipient scanning card / laughing.
8. EXAMPLES — cat, Labrador, dachshund. Same roast stage. Not just dogs.

# Listing videos (TWO, 3-15s each, NO AUDIO — Etsy strips it)

V1 Explain: pet photo → roast card → QR scan → pet appears on roast stage → recipient laughing. Burned-in captions.
V2 Comedy supercut: BISCUIT ROASTS JAMES cut MABEL ROASTS MUM cut GARY ROASTS DAD, audience insane. End: YOUR PET. YOUR ROAST.
"""


def build_listing(bundle_dir: str) -> dict:
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    order = manifest["order"]
    roast = manifest.get("roast", {})

    ldir = bdir / "listing"
    ldir.mkdir(exist_ok=True)
    (ldir / "title.txt").write_text(TITLE + "\n")
    (ldir / "description.md").write_text(description_for(order))
    (ldir / "personalization.json").write_text(json.dumps(PERSONALIZATION, indent=2))
    (ldir / "intensity_map.json").write_text(json.dumps(INTENSITY_MAP, indent=2))
    (ldir / "tags.txt").write_text("\n".join(TAGS) + "\n")
    (ldir / "image_shotlist.md").write_text(shotlist_for(manifest["slug"], roast))

    print(f"=== LISTING V1: {manifest['slug']} ===")
    print(f"  Title: {TITLE[:70]}...")
    print(f"  Tags: {len(TAGS)}")
    print(f"  Questions: {len(PERSONALIZATION['personalization_questions'])} (V1: four)")
    print(f"  Files: {ldir}/")
    return {"title": TITLE, "tags": TAGS}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.listing output/<slug>/")
        sys.exit(1)
    build_listing(sys.argv[1])
