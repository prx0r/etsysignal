"""Complete roast pipeline — pet photo → avatar → animation → gift page."""
import json
import os
import shutil
import sys
from pathlib import Path

ROAST_DIR = Path(__file__).parent
FREAK_DIR = Path("/home/ubuntu/freaktown/freaks")


def process_order(order_dir: str) -> dict:
    """Full pipeline: order → roast → bundle → gift page."""
    # 1. Load order
    with open(Path(order_dir) / "order.json") as f:
        order = json.load(f)
    
    # 2. Compile beats
    beats = compile_beats(order)
    
    # 3. Save FreakTown bundle
    slug, meta, offsets = save_freaktown_bundle(order, beats)
    
    # 4. Copy pet photos as portrait
    copy_pet_photos(order_dir, slug)
    
    # 5. Generate gift page URL
    gift_url = f"/gift/{slug}"
    
    return {
        "slug": slug,
        "duration": meta.get("duration_s"),
        "words": meta.get("word_count"),
        "beats": len(beats),
        "gift_url": gift_url,
        "pet": order.get("pet_name"),
        "recipient": order.get("recipient_name"),
    }


def compile_beats(order: dict) -> list[dict]:
    """Simple beat compiler — not comedy, just structure."""
    pet = order.get("pet_name", "Pet")
    recipient = order.get("recipient_name", "Friend")
    facts = order.get("roast_facts", [])
    signoff = order.get("signoff", f"Happy birthday!")
    
    beats = []
    beats.append({"id": "b1", "type": "setup", "text": f"{recipient}. It's me, {pet}.", "pause_after_ms": 500,
                  "performance": {"expression": "deadpan", "gesture": "still", "look": "camera"}})
    beats.append({"id": "b2", "type": "setup", "text": f"Apparently I've been asked to say something nice for your {order.get('occasion', 'birthday')}.",
                  "pause_after_ms": 800, "performance": {"expression": "skeptical", "gesture": "head_tilt", "look": "camera"}})
    
    for i, fact in enumerate(facts[:5]):
        beats.append({"id": f"b{i+3}", "type": "punchline", "text": f"{fact}",
                      "pause_after_ms": 900, "performance": {"expression": "grin", "gesture": "shrug", "look": "camera"}})
    
    beats.append({"id": "b_closer", "type": "closer", "text": signoff, "pause_after_ms": 1400,
                  "performance": {"expression": "celebrate", "gesture": "wave", "look": "camera"}})
    return beats


def save_freaktown_bundle(order: dict, beats: list[dict]) -> tuple:
    """Save as FreakTown bundle using existing _save_bundle."""
    sys.path.insert(0, "/home/ubuntu/freaktown")
    from app import _save_bundle
    
    character = {
        "name": order.get("pet_name", "Pet"),
        "species": order.get("pet_species", ""),
        "premise": f"{order.get('pet_name', 'Pet')} roasting {order.get('recipient_name', 'someone')}",
        "vibe": "overconfident",
        "voice": "en-GB-RyanNeural",
    }
    
    data = {
        "character": character,
        "beats": beats,
        "voice": "en-GB-RyanNeural",
        "style": "deadpan",
        "set_name": f"{order.get('pet_name', 'pet')}-roasts-{order.get('recipient_name', 'recipient')}",
    }
    
    slug, meta, offsets = _save_bundle(data)
    return slug, meta, offsets


def copy_pet_photos(order_dir: str, slug: str):
    """Copy pet photos as portrait.png for FreakTown."""
    bdir = FREAK_DIR / slug
    order_path = Path(order_dir)
    
    # Find first pet photo
    for f in ["pet-1.jpg", "pet-1.png", "pet-1.jpeg"]:
        src = order_path / f
        if src.exists():
            dst = bdir / "portrait.png"
            shutil.copy(src, dst)
            print(f"  Copied {f} → portrait.png")
            return
    
    # If no photos, create placeholder
    print("  No pet photos found, using default")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <order_dir>")
        sys.exit(1)
    result = process_order(sys.argv[1])
    print(json.dumps(result, indent=2))
