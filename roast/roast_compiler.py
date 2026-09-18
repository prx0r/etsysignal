"""Roast Compiler — turns RoastOrder into FreakTown-compatible beats."""
import json
import os
from typing import List, Dict


def compile_roast(order: dict) -> List[dict]:
    """Compile an order into FreakTown-compatible beats."""
    pet = order.get("pet_name", "your pet")
    recipient = order.get("recipient_name", "friend")
    occasion = order.get("occasion", "birthday")
    facts = order.get("roast_facts", [])
    tone = order.get("tone", "funny and cheeky")
    signoff = order.get("signoff", f"Happy birthday, you old fraud.")
    
    beats = []
    
    # Opening acknowledgement
    beats.append({
        "id": "b1",
        "type": "setup",
        "text": f"{recipient}. It's me, {pet}.",
        "pause_after_ms": 500,
        "performance": {
            "expression": "deadpan",
            "gesture": "still",
            "look": "camera"
        }
    })
    
    # Premise
    beats.append({
        "id": "b2",
        "type": "setup",
        "text": f"Apparently I've been asked to say something nice for your {occasion}.",
        "pause_after_ms": 800,
        "performance": {
            "expression": "skeptical",
            "gesture": "head_tilt",
            "look": "camera"
        }
    })
    
    # Roast beats from facts
    for i, fact in enumerate(facts[:5]):
        beats.append({
            "id": f"b{i+3}",
            "type": "punchline",
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
        "id": "b_affection",
        "type": "tag",
        "text": f"But honestly {recipient}... you do give decent treats.",
        "pause_after_ms": 1000,
        "performance": {
            "expression": "warm",
            "gesture": "still",
            "look": "soft"
        }
    })
    
    # Signoff
    beats.append({
        "id": "b_signoff",
        "type": "closer",
        "text": signoff,
        "pause_after_ms": 1400,
        "performance": {
            "expression": "celebrate",
            "gesture": "wave",
            "look": "camera"
        }
    })
    
    return beats


def generate_roast_text(beats: List[dict]) -> str:
    """Generate full roast text from beats."""
    parts = []
    for beat in beats:
        parts.append(beat["text"])
        parts.append("")  # pause
    return "\n".join(parts)


if __name__ == "__main__":
    # Load demo order
    order_path = os.path.join(os.path.dirname(__file__), "demo_orders", "buster-001", "order.json")
    with open(order_path) as f:
        order = json.load(f)
    
    beats = compile_roast(order)
    print(json.dumps(beats, indent=2))
    print()
    print("=== FULL ROAST ===")
    print(generate_roast_text(beats))
