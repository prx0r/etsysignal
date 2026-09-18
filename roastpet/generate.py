#!/usr/bin/env python3
"""roastpet generate — Full pipeline from Etsy order to character bundle.

Usage:
    python -m roastpet.generate roast/demo_orders/buster-001/
    python -m roastpet.generate roast/demo_orders/buster-001/ --reroll meaner
"""
import asyncio
import json
import os
import shutil
import sys
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FREAKTOWN = Path("/home/ubuntu/freaktown")
sys.path.insert(0, str(FREAKTOWN))

OUT_DIR = REPO_ROOT / "output"

# ── Voice presets ────────────────────────────────────────────────────
VOICE_PRESETS = {
    "deadpan":    "en-GB-RyanNeural",
    "savage":     "en-GB-ThomasNeural",
    "unhinged":   "en-US-GuyNeural",
    "gentle":     "en-AU-WilliamNeural",
    "movie_trailer": "en-US-ChristopherNeural",
}

# ── Walkout genre presets ────────────────────────────────────────────
WALKOUT_PRESETS = {
    "deadpan":    {"genre": "jazz",       "mood": "chill",       "energy": "medium", "shape": "hit"},
    "savage":     {"genre": "rock",       "mood": "menacing",    "energy": "high",   "shape": "sting"},
    "unhinged":   {"genre": "comedy",     "mood": "chaotic",     "energy": "unhinged","shape": "hit"},
    "gentle":     {"genre": "orchestral", "mood": "confident",   "energy": "medium", "shape": "swell"},
    "movie_trailer": {"genre": "electronic","mood": "heroic",    "energy": "high",   "shape": "sting"},
}


def load_order(order_dir: str) -> dict:
    """Load order.json from an order directory."""
    order_path = Path(order_dir) / "order.json"
    if not order_path.exists():
        raise FileNotFoundError(f"No order.json in {order_dir}")
    with open(order_path) as f:
        return json.load(f)


# ── Style-specific roast templates ───────────────────────────────
# Each style gets its own joke architecture + affection line.
# The reroll direction selects the style; the pairwise Take 1 vs Take 2
# comparison is the training signal (A vs B → kept).
STYLE_ROAST_TEMPLATES = {
    "savage": [
        "{fact}. But sure, you're doing great.",
        "Let me tell you about {fact}. Actually, no — the audience isn't ready.",
        "{fact}. I'd intervene, but honestly it's more entertaining to watch.",
        "And don't get me started on {fact}. The whole neighbourhood knows.",
        "{fact}. I've reported this to the authorities. Multiple times.",
    ],
    "deadpan": [
        "{fact}. Fascinating. Tell me more. Actually, don't.",
        "I have reviewed the evidence regarding {fact}. It is worse than you think.",
        "{fact}. I stared at the wall for an hour after learning this.",
        "Noted: {fact}. Filed under disappointments.",
        "{fact}. The audience has gone quiet. Wise.",
    ],
    "unhinged": [
        "{fact}?! BRO. THE DOGS IN THE BACK ROW JUST FAINTED.",
        "STOP. Everybody stop. Did you hear about {fact}? CHAOS.",
        "{fact}!!! I need to lie down. Somebody get me a treat.",
        "BREAKING NEWS: {fact}. More at eleven. WOOF.",
        "{fact}. I'm calling the band. Play us out, boys!",
    ],
    "gentle": [
        "{fact}. And honestly? We love you for it. Mostly.",
        "You do {fact}, and somehow we all still adore you.",
        "{fact}. It's part of your charm. A strange part, but still.",
        "Let's be honest about {fact}. It's funny because it's true, sweetie.",
        "{fact}. The whole family laughs about it. With love. Mostly.",
    ],
    "movie_trailer": [
        "In a world... where {fact}... one dog dared to speak.",
        "This summer: {fact}. No one is safe. Especially not you.",
        "{fact}. Coming soon to a living room near you.",
        "He saw {fact}. He could not stay silent. This is his story.",
        "{fact}. Rated R for roast.",
    ],
}

STYLE_AFFECTION = {
    "savage": "But honestly, {recipient}... you do give excellent treats. And your lap is... adequate.",
    "deadpan": "{recipient}. Your treat consistency is statistically acceptable. Well done.",
    "unhinged": "{recipient}!!! YOU ARE THE BEST HUMAN EVER!!! I LOVE YOU!!! TREATS NOW!!!",
    "gentle": "{recipient}, you're my favourite human in the whole world, and I mean that sincerely.",
    "movie_trailer": "But through it all... {recipient}... you were always... there with snacks.",
}

# Reroll directions (customer-facing) → generation style.
REROLL_DIRECTIONS = {
    "funnier": "unhinged",
    "meaner": "savage",
    "cuter": "gentle",
    "deadpan": "deadpan",
    "trailer": "movie_trailer",
}


def compile_roast(order: dict, style: str = "savage") -> list[dict]:
    """Compile order into Late Late Dog Show beats.

    This is the comedy engine adapter — takes Etsy order data and produces
    the beat script that FreakTown's delivery sequencer renders.
    """
    pet = order.get("pet_name", "Buster")
    recipient = order.get("recipient_name", "James")
    occasion = order.get("occasion", "birthday")
    facts = order.get("roast_facts", [])
    tone = order.get("tone", "savage but affectionate")
    signoff = order.get("signoff", f"Happy {occasion}, {recipient}.")

    beats = []

    # ── ANNOUNCER BEAT (spoken, TTS-safe) ──────────────────────
    beats.append({
        "id": "announcer",
        "type": "setup",
        "text": f"Tonight on the Late Late Dog Show... {pet}!",
        "pause_after_ms": 1200,
        "performance": {"expression": "neutral", "gesture": "still", "look": "audience"},
    })

    # ── HOST INTRO ───────────────────────────────────────────────
    beats.append({
        "id": "host_intro",
        "type": "setup",
        "text": f"Welcome back! Tonight's special guest — fresh from destroying the couch — it's {pet}!",
        "pause_after_ms": 1500,
        "performance": {"expression": "smile", "gesture": "wave", "look": "guest"},
    })

    # ── HOST QUESTION ────────────────────────────────────────────
    beats.append({
        "id": "host_question",
        "type": "setup",
        "text": f"So, {pet}, tell us about {recipient}.",
        "pause_after_ms": 800,
        "performance": {"expression": "curious", "gesture": "lean_in", "look": "guest"},
    })

    # ── PET OPENER ───────────────────────────────────────────────
    opener = f"{recipient}? Oh, where do I even start."
    beats.append({
        "id": "pet_opener",
        "type": "setup",
        "text": opener,
        "pause_after_ms": 600,
        "performance": {"expression": "deadpan", "gesture": "sigh", "look": "camera"},
    })

    # ── PET PREMISE ──────────────────────────────────────────────
    premise = f"Apparently it's your {occasion}. Huge achievement. You've survived another year despite needing me to supervise literally every meal."
    beats.append({
        "id": "pet_premise",
        "type": "escalation",
        "text": premise,
        "pause_after_ms": 1000,
        "performance": {"expression": "skeptical", "gesture": "head_tilt", "look": "camera"},
    })

    # ── ROAST BEATS FROM FACTS (style-specific architecture) ──────
    templates = STYLE_ROAST_TEMPLATES.get(style, STYLE_ROAST_TEMPLATES["savage"])
    for i, fact in enumerate(facts[:5]):
        template = templates[i % len(templates)]
        text = template.format(fact=fact)
        beat_id = f"roast_{i+1}"
        beats.append({
            "id": beat_id,
            "type": "punchline",
            "text": text,
            "pause_after_ms": 1200 if i < len(facts) - 1 else 1500,
            "performance": {
                "expression": "grin" if i % 2 == 0 else "deadpan",
                "gesture": "point" if i % 2 == 0 else "shrug",
                "look": "camera",
            },
        })

    # ── AFFECTION TURN (style-specific) ──────────────────────────
    affection_text = STYLE_AFFECTION.get(style, STYLE_AFFECTION["savage"]).format(recipient=recipient)
    beats.append({
        "id": "affection",
        "type": "tag",
        "text": affection_text,
        "pause_after_ms": 1200,
        "performance": {"expression": "warm", "gesture": "still", "look": "soft"},
    })

    # ── HOST FOLLOWUP ────────────────────────────────────────────
    beats.append({
        "id": "host_followup",
        "type": "setup",
        "text": f"Everybody — {pet} has spoken! Give it up for {pet}!",
        "pause_after_ms": 1000,
        "performance": {"expression": "celebrate", "gesture": "applaud", "look": "audience"},
    })

    # ── SIGNOFF ──────────────────────────────────────────────────
    beats.append({
        "id": "signoff",
        "type": "closer",
        "text": signoff,
        "pause_after_ms": 2000,
        "performance": {"expression": "smile", "gesture": "wave", "look": "camera"},
    })

    return beats


def build_character(order: dict, voice: str, walkout: dict) -> dict:
    """Build the character dict for _save_bundle."""
    pet_name = order.get("pet_name", "Pet")
    recipient = order.get("recipient_name", "someone")
    occasion = order.get("occasion", "birthday")
    species = order.get("pet_species", order.get("pet_breed", "dog"))

    return {
        "character": {
            "name": pet_name,
            "species": species,
            "premise": f"{pet_name} roasting {recipient} for {occasion}",
            "vibe": "overconfident",
            "voice": voice,
        },
        "voice": voice,
        "style": order.get("tone", "savage but affectionate"),
        "set_name": f"{pet_name.lower()}-roasts-{recipient.lower()}",
        "walkout": walkout,
        "creator": "roastpet-pipeline",
    }


def copy_pet_photos(order_dir: Path, bundle_dir: Path):
    """Copy customer pet photos into the bundle for reference.

    Handles both layouts:
      - demo_orders/buster-001/*.jpg (flat)
      - checkpoint 02_customer_uploads/buster-001/raw/*.png (raw subdir)
    """
    photos_dir = bundle_dir / "photos"
    copied = 0
    for candidate in [order_dir / "raw", order_dir]:
        if not candidate.exists():
            continue
        for f in sorted(candidate.iterdir()):
            if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                photos_dir.mkdir(exist_ok=True)
                shutil.copy(f, photos_dir / f.name)
                copied += 1
        if copied:
            break


def generate_card_spec(order: dict, slug: str) -> dict:
    """Generate the card artwork specification (Prodigi-ready)."""
    pet = order.get("pet_name", "Buster")
    recipient = order.get("recipient_name", "James")
    occasion = order.get("occasion", "birthday")

    return {
        "product": "fine_art_5x7",
        "slug": slug,
        "url": f"roast.pet/{slug}",
        "front": {
            "headline": f"HAPPY {occasion.upper()} FROM\nSOMEONE WITH STANDARDS",
            "photo": "pet_01_front_face.png",
        },
        "inside_left": {
            "text": f"Tonight's Special Guest\n\n{pet}\n\nThe Late Late Dog Show",
        },
        "inside_right": {
            "text": f"{pet} has prepared some remarks.",
            "qr_url": f"https://roast.pet/{slug}",
            "cta": "WATCH MY ROAST →",
        },
        "back": {
            "brand": "roast.pet",
        },
    }


def run_pipeline(order_dir: str, reroll_style: str = None) -> dict:
    """Full pipeline: order → roast → bundle → card spec → manifest.

    Returns the full output manifest.
    """
    order_path = Path(order_dir)
    order = load_order(order_dir)

    pet_name = order.get("pet_name", "Pet")
    recipient = order.get("recipient_name", "someone")
    tone = order.get("tone", "deadpan")

    # ── 1. Select voice + walkout from tone/style ────────────────
    # reroll_style may be a customer direction (funnier/meaner/cuter)
    # or a raw style name. Directions map to styles.
    if reroll_style:
        style_key = REROLL_DIRECTIONS.get(reroll_style.lower(), reroll_style.lower())
    else:
        style_key = tone.split()[0].lower()
    if style_key not in VOICE_PRESETS:
        style_key = "deadpan"
    voice = VOICE_PRESETS[style_key]
    walkout = {**WALKOUT_PRESETS.get(style_key, WALKOUT_PRESETS["deadpan"]), "seed": 42}

    print(f"=== LATE LATE DOG SHOW PIPELINE ===")
    print(f"  Pet:     {pet_name}")
    print(f"  Roasting: {recipient}")
    print(f"  Style:   {style_key}")
    print(f"  Voice:   {voice}")
    print()

    # ── 2. Compile roast beats (style-specific) ──────────────────
    print("Step 1: Compiling roast beats...")
    beats = compile_roast(order, style=style_key)
    print(f"  Generated {len(beats)} beats:")
    for b in beats:
        text_preview = b["text"][:70] + "..." if len(b["text"]) > 70 else b["text"]
        print(f"    [{b['type']:12s}] {text_preview}")
    print()

    # ── 3. Build character + save bundle via FreakTown ───────────
    print("Step 2: Saving bundle via FreakTown...")
    from app import _save_bundle

    bundle_data = build_character(order, voice, walkout)
    bundle_data["beats"] = beats

    slug, meta, offsets = _save_bundle(bundle_data)
    bundle_dir = FREAKTOWN / "freaks" / slug
    print(f"  Bundle: freaks/{slug}/")
    print(f"  Duration: {meta.get('duration_s', '?')}s")
    print(f"  Words: {meta.get('word_count', '?')}")
    print(f"  Beats: {meta.get('beat_count', '?')}")
    print()

    # ── 4. Copy pet photos into bundle ───────────────────────────
    print("Step 3: Copying customer photos...")
    copy_pet_photos(order_path, bundle_dir)
    photo_count = len(list((bundle_dir / "photos").glob("*"))) if (bundle_dir / "photos").exists() else 0
    print(f"  Copied {photo_count} photos")
    print()

    # ── 5. Generate card spec ────────────────────────────────────
    print("Step 4: Generating card specification...")
    card_spec = generate_card_spec(order, slug)
    (bundle_dir / "card_spec.json").write_text(json.dumps(card_spec, indent=2))
    print(f"  Card spec: {bundle_dir / 'card_spec.json'}")
    print()

    # ── 6. Copy bundle to output dir ─────────────────────────────
    OUT_DIR.mkdir(exist_ok=True)
    output_bundle = OUT_DIR / slug
    if output_bundle.exists():
        shutil.rmtree(output_bundle)
    shutil.copytree(bundle_dir, output_bundle)
    print(f"Step 5: Copied to output/{slug}/")
    print()

    # ── 7. Write manifest ────────────────────────────────────────
    manifest = {
        "pipeline": "roastpet-v0",
        "order": order,
        "slug": slug,
        "style": style_key,
        "voice": voice,
        "walkout": walkout,
        "bundle_dir": str(output_bundle),
        "card_spec": card_spec,
        "beats": [{"id": b["id"], "type": b["type"], "text": b["text"]} for b in beats],
        "duration_s": meta.get("duration_s"),
        "word_count": meta.get("word_count"),
        "beat_count": meta.get("beat_count"),
        "photos_copied": photo_count,
        "reroll_of": reroll_style,
    }
    manifest_path = output_bundle / "pipeline_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print("=== PIPELINE COMPLETE ===")
    print(f"  Output: output/{slug}/")
    print(f"  Audio:  output/{slug}/set.wav")
    print(f"  Avatar: output/{slug}/avatar.glb")
    print(f"  Card:   output/{slug}/card_spec.json")
    print(f"  View:   /f/{slug}")
    print()

    return manifest


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="roastpet Late Late Dog Show pipeline")
    parser.add_argument("order_dir", help="Path to order directory (must contain order.json)")
    parser.add_argument("--reroll", dest="reroll_style", default=None,
                        help="Reroll with different style: deadpan, savage, unhinged, gentle, movie_trailer")
    args = parser.parse_args()
    run_pipeline(args.order_dir, args.reroll_style)
