"""Roast Compiler — turns RoastBrief into executable roast script."""
import json
from typing import List, Dict


def compile_roast(brief: dict) -> dict:
    """Compile a RoastBrief into a roast script."""
    pet = brief.get("pet", {})
    recipient = brief.get("recipient", {})
    facts = brief.get("roast_material", [])
    tone = brief.get("tone", "funny_cheeky")
    custom = brief.get("custom_message", "")
    
    pet_name = pet.get("name", "your pet")
    recipient_name = recipient.get("name", "friend")
    occasion = recipient.get("occasion", "birthday")
    
    # Build roast beats from facts
    roast_beats = []
    for fact in facts[:6]:
        roast_beats.append(f"{fact}... honestly, how do you live with yourself?")
    
    # Build script
    script = {
        "intro": f"Hello {recipient_name}. It's me, {pet_name}.",
        "premise": f"Apparently I've been asked to say something nice for your {occasion}.",
        "roast_beats": roast_beats,
        "affection_turn": f"But honestly {recipient_name}... you do give decent treats.",
        "signoff": custom or f"Happy birthday, you old fraud. Love, {pet_name}.",
        "duration_estimate": f"{30 + len(roast_beats) * 5} seconds",
    }
    
    return script


def generate_roast_text(script: dict) -> str:
    """Generate full roast text from script."""
    parts = [
        script["intro"],
        "",
        script["premise"],
        "",
    ]
    for beat in script["roast_beats"]:
        parts.append(beat)
        parts.append("")
    parts.append(script["affection_turn"])
    parts.append("")
    parts.append(script["signoff"])
    return "\n".join(parts)


# Example usage
if __name__ == "__main__":
    brief = {
        "pet": {"name": "Buster", "species": "dog", "breed": "dachshund"},
        "recipient": {"name": "James", "relationship": "dad", "occasion": "50th birthday"},
        "roast_material": ["supports Arsenal", "thinks he's good at golf", "snores loudly"],
        "tone": "funny and cheeky",
        "custom_message": "Happy birthday from Sophie and Buster"
    }
    
    script = compile_roast(brief)
    print(json.dumps(script, indent=2))
    print()
    print("=== FULL ROAST ===")
    print(generate_roast_text(script))
