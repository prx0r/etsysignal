#!/usr/bin/env python3
"""roastpet listing — Etsy listing pack from a built bundle.

Usage:
    python -m roastpet.listing output/<slug>/

Writes listing/ into the bundle:
  title.txt, description.md, personalization.json, tags.txt,
  image_shotlist.md

Launch decision (variation_plan.json + strategy):
  ONE listing = ONE concept (Late Late Dog Show). No show-style selector
  in v0 — buyer personalizes content, not layout. Show styles become
  separate listings later (Breaking News, Awards Night, Christmas).
"""
import json
import sys
from pathlib import Path


TITLE = "Personalized Pet Roast Card + Video | Your Dog on a Late-Night Show | Funny Custom Birthday Card From Your Pet"

TAGS = [
    "personalized pet roast", "funny dog birthday card", "custom pet video",
    "dog late night show", "pet comedy gift", "funny birthday card for him",
    "dog dad gift", "talking pet video", "custom qr card", "pet lover gift",
    "funny 50th birthday", "dog roast video", "personalised pet gift",
]

PERSONALIZATION = {
    "personalization_questions": [
        {
            "question_type": "labeled_upload",
            "question_text": "Pet photos",
            "instructions": "Use clear photos of the same pet. Avoid filters, screenshots, costumes and cropped ears.",
            "required": True,
            "max_allowed_files": 4,
            "options": [{"label": "Front face"}, {"label": "Full body"},
                        {"label": "Side view"}, {"label": "Favourite photo"}],
        },
        {
            "question_type": "text_input",
            "question_text": "Pet and birthday details",
            "instructions": "Pet name; recipient name; age; relation. Example: Buster; James; 50; Dad.",
            "required": True,
            "max_allowed_characters": 160,
        },
        {
            "question_type": "text_input",
            "question_text": "Give us the gossip",
            "instructions": "Share 3-8 specific habits, stories or running jokes. Include funny pet details too.",
            "required": True,
            "max_allowed_characters": 1024,
        },
        {
            "question_type": "dropdown",
            "question_text": "How savage should it be?",
            "required": True,
            "options": [{"label": "Sweet"}, {"label": "Cheeky"},
                        {"label": "Savage"}, {"label": "Unhinged"}],
        },
        {
            "question_type": "text_input",
            "question_text": "Birthday sign-off",
            "instructions": "What should your pet say at the end? Example: Happy 50th Dad - love Sophie and Buster.",
            "required": False,
            "max_allowed_characters": 300,
        },
    ]
}

# Dropdown label → pipeline style (reroll.py directions).
SAVAGE_MAP = {"Sweet": "gentle", "Cheeky": "deadpan",
              "Savage": "savage", "Unhinged": "unhinged"}


def description_for(order: dict) -> str:
    pet = order.get("pet_name", "your pet")
    return f"""YOUR PET. THEIR OWN COMEDY SHOW.

Upload photos of {pet}-style greatness and give us the gossip. We turn your pet into the guest of honour on their very own late-night show — then print it all on a premium birthday card with a QR code that plays the roast.

WHAT YOU GET
- Premium 5x7 Fine Art birthday card, personalised with your pet's photo and headline
- A private show link (QR code inside the card): your pet roasts the recipient, late-night-show style
- 1 FREE directed reroll — funnier, meaner or cuter — you keep both takes

HOW IT WORKS
1. Upload 4 photos of your pet (front face, full body, side view, favourite)
2. Tell us the gossip — 3-8 specific habits, stories, running jokes
3. Pick how savage it should be
4. We generate the show, print the card and ship it

PLEASE UPLOAD THE SAME PET IN ALL FOUR SLOTS.
- Front face — eyes visible, ears/head not cropped
- Full body — all four legs/body shape visible if possible
- Side view — useful for building the avatar
- Favourite photo — personality/reference

Best results: daylight, sharp image, no filters or stickers. Phone photos are fine.

The card design shown is the design you receive. You personalize the content, not the layout — so what you see is what arrives, starring your pet.
"""


def shotlist_for(slug: str) -> str:
    return f"""# Listing image shotlist — {slug}

1. HERO — physical 5x7 card at 3/4 angle + envelope, huge pet face, printed headline readable. No marketing overlay.
2. MAGIC — card → QR → phone showing the Late Late Dog Show.
3. SHOW — phone close-up: host, guest pet, dog audience mid-eruption. Giant subtitle.
4. CARD OPEN — physical card open, QR visible inside right.
5. PERSONALIZATION — photos + gossip facts → character.
6. REROLL — Take 1 ↔ Take 2, "1 FREE REROLL".
7. GIFT REACTION — someone opening the card.
8. DIMENSIONS — card size, 324gsm stock, texture.
9. MORE SHOWS — coming soon: News, Awards Night, Christmas.
10. TURNAROUND — production + delivery times, what's included.

Video (3-15s, NO AUDIO — Etsy strips it): photo → card → phone scan → show erupts → YOUR PET. THEIR OWN COMEDY SHOW.
"""


def build_listing(bundle_dir: str) -> dict:
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    order = manifest["order"]

    ldir = bdir / "listing"
    ldir.mkdir(exist_ok=True)
    (ldir / "title.txt").write_text(TITLE + "\n")
    (ldir / "description.md").write_text(description_for(order))
    (ldir / "personalization.json").write_text(json.dumps(PERSONALIZATION, indent=2))
    (ldir / "savage_map.json").write_text(json.dumps(SAVAGE_MAP, indent=2))
    (ldir / "tags.txt").write_text("\n".join(TAGS) + "\n")
    (ldir / "image_shotlist.md").write_text(shotlist_for(manifest["slug"]))

    print(f"=== LISTING: {manifest['slug']} ===")
    print(f"  Title: {TITLE[:70]}...")
    print(f"  Tags: {len(TAGS)}")
    print(f"  Questions: {len(PERSONALIZATION['personalization_questions'])}")
    print(f"  Files: {ldir}/")
    return {"title": TITLE, "tags": TAGS}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.listing output/<slug>/")
        sys.exit(1)
    build_listing(sys.argv[1])
