"""Gift Roast — orchestrates pet roast generation using FreakTown primitives.

Usage:
    python gift_roast.py demo_orders/buster-001/
"""
import json
import os
import sys
import shutil
from pathlib import Path

# Add FreakTown to path
sys.path.insert(0, "/home/ubuntu/freaktown")

ROAST_DIR = Path(__file__).parent
ORDERS_DIR = ROAST_DIR / "demo_orders"


def load_order(order_dir: str) -> dict:
    """Load a RoastOrder from directory."""
    order_path = Path(order_dir) / "order.json"
    with open(order_path) as f:
        return json.load(f)


def compile_beats(order: dict) -> list[dict]:
    """Compile order into FreakTown-compatible beats."""
    pet = order.get("pet_name", "your pet")
    recipient = order.get("recipient_name", "friend")
    facts = order.get("roast_facts", [])
    signoff = order.get("signoff", f"Happy birthday, you old fraud.")
    
    beats = []
    
    # Opening
    beats.append({
        "id": "b1", "type": "setup",
        "text": f"{recipient}. It's me, {pet}.",
        "pause_after_ms": 500,
        "performance": {"expression": "deadpan", "gesture": "still", "look": "camera"}
    })
    
    # Premise
    beats.append({
        "id": "b2", "type": "setup",
        "text": f"Apparently I've been asked to say something nice for your {order.get('occasion', 'birthday')}.",
        "pause_after_ms": 800,
        "performance": {"expression": "skeptical", "gesture": "head_tilt", "look": "camera"}
    })
    
    # Roast beats
    for i, fact in enumerate(facts[:5]):
        beats.append({
            "id": f"b{i+3}", "type": "punchline",
            "text": f"{fact}... honestly, how do you live with yourself?",
            "pause_after_ms": 900 if i < len(facts) - 1 else 1200,
            "performance": {
                "expression": "grin" if i % 2 == 0 else "deadpan",
                "gesture": "shrug" if i % 2 == 0 else "point",
                "look": "camera"
            }
        })
    
    # Affection turn
    beats.append({
        "id": "b_affection", "type": "tag",
        "text": f"But honestly {recipient}... you do give decent treats.",
        "pause_after_ms": 1000,
        "performance": {"expression": "warm", "gesture": "still", "look": "soft"}
    })
    
    # Signoff
    beats.append({
        "id": "b_signoff", "type": "closer",
        "text": signoff,
        "pause_after_ms": 1400,
        "performance": {"expression": "celebrate", "gesture": "wave", "look": "camera"}
    })
    
    return beats


def save_bundle(order: dict, beats: list[dict]) -> str:
    """Save as FreakTown bundle using existing _save_bundle logic."""
    from app import _save_bundle
    
    character = {
        "name": order.get("pet_name", "Pet"),
        "species": order.get("pet_species", ""),
        "premise": f"{order.get('pet_name', 'Pet')} roasting {order.get('recipient_name', 'someone')} for {order.get('occasion', 'birthday')}",
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


def run_gift_roast(order_dir: str):
    """Main entry point: load order → compile → save bundle."""
    print(f"Loading order from {order_dir}...")
    order = load_order(order_dir)
    
    print(f"Compiling beats for {order.get('pet_name', 'pet')} roasting {order.get('recipient_name', 'someone')}...")
    beats = compile_beats(order)
    
    print(f"Generated {len(beats)} beats")
    for b in beats:
        print(f"  [{b['type']}] {b['text'][:60]}...")
    
    print()
    print("Saving bundle...")
    slug, meta, offsets = save_bundle(order, beats)
    
    print(f"Bundle saved: freaks/{slug}/")
    print(f"  Duration: {meta.get('duration_s', '?')}s")
    print(f"  Words: {meta.get('word_count', '?')}")
    print(f"  Beats: {meta.get('beat_count', '?')}")
    print()
    print(f"View at: /f/{slug}")
    return slug


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gift_roast.py <order_dir>")
        sys.exit(1)
    run_gift_roast(sys.argv[1])
