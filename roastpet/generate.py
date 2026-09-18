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

from .comedy import normalize_order, build_roast_json, INTENSITY_MAP
from .comedy import ROAST_JSON_SCHEMA  # noqa: F401 (contract, re-exported)

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
        "Here's the thing about {recipient}: {Fact}. Actually, no — the audience isn't ready.",
        "{Fact}. I'd intervene, but honestly it's more entertaining to watch.",
        "And don't get me started on {fact}. The whole neighbourhood knows.",
        "{Fact}. I've reported this to the authorities. Multiple times.",
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

# Reroll reasons (customer-facing, northstar.md) → generation style.
# None = keep Take 1's style; the reason changes something else
# (fact window, voice, or a recorded free-text note).
REROLL_DIRECTIONS = {
    "funnier": "unhinged",
    "meaner": "savage",
    "gentler": "gentle",
    "cuter": "gentle",
    "deadpan": "deadpan",
    "trailer": "movie_trailer",
    "more personal": None,
    "different voice": None,
    "something else": None,
}

# Voice cycle for "different voice" rerolls.
VOICE_CYCLE = list(VOICE_PRESETS.values())


def compile_roast(order: dict, style: str = "savage",
                  fact_start: int = 0) -> tuple[list[dict], dict]:
    """Compile order → canonical roast.json → V1 podium beats.

    V1 grammar (northstar.md): sting → opening → 3 bits → callback →
    signoff. Single performer at the podium, no host. Reactions become
    pause length + gesture (bark SFX is mixed at show-render time).
    Returns (beats, roast_json). Every renderer consumes roast.json.
    """
    norder = normalize_order(order)
    pet = norder["pet"]["name"]
    target = norder["target"]["name"]
    signoff_default = f"Happy birthday, {target}."

    roast = build_roast_json(norder, STYLE_ROAST_TEMPLATES, fact_start=fact_start)
    roast["signoff"] = order.get("signoff") or signoff_default

    REACTION_PAUSE = {"big_bark": 1500, "reaction_shot": 1200, "crowd_loses_it": 2000}

    beats = [
        {
            "id": "sting",
            "type": "setup",
            "text": f"Roast.pet presents... {pet}!",
            "pause_after_ms": 1000,
            "performance": {"expression": "neutral", "gesture": "still", "look": "audience"},
        },
        {
            "id": "opening",
            "type": "setup",
            "text": roast["opening"],
            "pause_after_ms": 700,
            "performance": {"expression": "deadpan", "gesture": "tap_mic", "look": "camera"},
        },
    ]
    for i, bit in enumerate(roast["bits"]):
        beats.append({
            "id": f"bit_{i+1}",
            "type": "punchline",
            "text": f"{bit['setup']} {bit['punchline']}",
            "pause_after_ms": REACTION_PAUSE.get(bit["reaction"], 1200),
            "performance": {
                "expression": "grin" if i % 2 == 0 else "deadpan",
                "gesture": "point" if i % 2 == 0 else "shrug",
                "look": "camera",
                "reaction": bit["reaction"],
            },
        })
    beats += [
        {
            "id": "callback",
            "type": "tag",
            "text": roast["callback"],
            "pause_after_ms": 1200,
            "performance": {"expression": "smirk", "gesture": "point", "look": "camera"},
        },
        {
            "id": "signoff",
            "type": "closer",
            "text": roast["signoff"],
            "pause_after_ms": 2000,
            "performance": {"expression": "warm", "gesture": "bow", "look": "camera"},
        },
    ]
    return beats, roast


def build_character(order: dict, voice: str, walkout: dict) -> dict:
    """Build the character dict for _save_bundle (accepts V1 or legacy order)."""
    norder = normalize_order(order)
    pet_name = norder["pet"]["name"]
    recipient = norder["target"]["name"]
    occasion = order.get("occasion", "birthday")
    species = order.get("pet_species", order.get("pet_breed", "dog"))

    return {
        "character": {
            "name": pet_name,
            "species": species,
            "premise": f"{pet_name} roasting {recipient} at the podium ({occasion})",
            "vibe": "overconfident",
            "voice": voice,
        },
        "voice": voice,
        "style": f"roast_v1/{norder['intensity']}",
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
    norder = normalize_order(order)
    pet = norder["pet"]["name"]
    recipient = norder["target"]["name"]
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


def run_pipeline(order_dir: str, reroll_style: str = None,
                 fact_start: int = 0, voice_override: str = None,
                 note: str = None, intensity_override: str = None) -> dict:
    """Full pipeline: order → roast.json → beats → bundle → card → manifest.

    Returns the full output manifest. roast.json is written into the
    bundle and is what every renderer consumes (northstar.md).
    """
    order_path = Path(order_dir)
    order = load_order(order_dir)
    norder = normalize_order(order)
    if intensity_override:
        norder["intensity"] = intensity_override

    pet_name = norder["pet"]["name"]
    recipient = norder["target"]["name"]

    # ── 1. Select voice + walkout ──────────────────────────────────
    # reroll_style may be a V1 reason (funnier/meaner/gentler/...) or a
    # raw style name. Reasons map to styles via REROLL_DIRECTIONS;
    # None keeps the order intensity (reason changes facts/voice/note).
    if reroll_style:
        mapped = REROLL_DIRECTIONS.get(reroll_style.lower(), reroll_style.lower())
        style_key = mapped or INTENSITY_MAP.get(norder["intensity"], "deadpan")
    else:
        style_key = INTENSITY_MAP.get(norder["intensity"], "deadpan")
    if style_key not in VOICE_PRESETS:
        style_key = "deadpan"
    voice = voice_override or VOICE_PRESETS[style_key]
    walkout = {**WALKOUT_PRESETS.get(style_key, WALKOUT_PRESETS["deadpan"]), "seed": 42}

    print(f"=== ROAST.PET V1 PIPELINE ===")
    print(f"  Pet:      {pet_name}")
    print(f"  Roasting: {recipient}")
    print(f"  Intensity:{norder['intensity']} → style {style_key}")
    print(f"  Voice:    {voice}")
    print()

    # ── 2. Compile roast.json → beats ──────────────────────────────
    print("Step 1: Compiling roast.json → beats...")
    beats, roast = compile_roast(order, style=style_key, fact_start=fact_start)
    print(f"  Headline: {roast['headline'][:80]}")
    print(f"  Card line: {roast['card_line']}")
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
    # roast.json goes into the bundle: it is the canonical artifact.
    (bundle_dir / "roast.json").write_text(json.dumps(roast, indent=2))
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
        "pipeline": "roastpet-v1",
        "order": order,
        "normalized_order": norder,
        "slug": slug,
        "style": style_key,
        "voice": voice,
        "walkout": walkout,
        "bundle_dir": str(output_bundle),
        "card_spec": card_spec,
        "roast": roast,
        "beats": [{"id": b["id"], "type": b["type"], "text": b["text"]} for b in beats],
        "duration_s": meta.get("duration_s"),
        "word_count": meta.get("word_count"),
        "beat_count": meta.get("beat_count"),
        "photos_copied": photo_count,
        "reroll_of": reroll_style,
        "fact_start": fact_start,
        "customer_note": note,
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
                        help="V1 reason: funnier | meaner | gentler | more personal | different voice | something else")
    args = parser.parse_args()
    run_pipeline(args.order_dir, args.reroll_style)
