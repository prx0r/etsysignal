#!/usr/bin/env python3
"""roastpet comedy — Canonical roast.json engine.

V1 (northstar.md): the order becomes ONE structured object, generation
produces roast.json, and roast.json is what EVERY renderer consumes.
Frontier models are replaceable renderers; roast.json is the contract.

Order shapes accepted (normalized to V1):
  V1:      {"pet": {"name"}, "target": {"name","relationship"},
            "facts": [...], "intensity": "playful|spicy|savage"}
  Legacy:  {"pet_name", "recipient_name", "relationship",
            "roast_facts", "tone"}

roast.json:
  {"headline", "opening", "bits": [{"setup","punchline","reaction"}],
   "callback", "signoff", "card_line", "visual": {"pet","stage": "roast_v1"}}
"""
from __future__ import annotations

STAGE = "roast_v1"

# V1 dropdown → generation style.
INTENSITY_MAP = {
    "playful": "gentle",
    "spicy": "deadpan",
    "savage": "savage",
}

# Legacy free-text tones → V1 intensity.
LEGACY_TONE_MAP = {
    "savage": "savage",
    "unhinged": "savage",
    "cheeky": "spicy",
    "deadpan": "spicy",
    "sweet": "playful",
    "gentle": "playful",
}

ROAST_JSON_SCHEMA = {
    "headline": "str — the roast title, one joke (card + listing hero)",
    "opening": "str — cold open, ~10 words ('James. My owner.')",
    "bits": "list[{setup, punchline, reaction}] — 3 bits, strongest last",
    "callback": "str — callback to bit #1",
    "signoff": "str — birthday close from the order",
    "card_line": "str — ONE killer line ≤12 words, the card teaser",
    "visual": "{pet, stage} — stage is always roast_v1 in V1",
}

REACTIONS = ["big_bark", "reaction_shot", "crowd_loses_it"]


def normalize_order(order: dict) -> dict:
    """Normalize legacy or V1 order → V1 structured order."""
    if "pet" in order and "facts" in order:
        intensity = str(order.get("intensity", "spicy")).lower()
        return {
            "pet": {"name": order["pet"].get("name", "Buster")},
            "target": {
                "name": order["target"].get("name", "James"),
                "relationship": order["target"].get("relationship", "owner"),
            },
            "facts": list(order.get("facts", [])),
            "intensity": intensity if intensity in INTENSITY_MAP else "spicy",
        }
    # Legacy demo shape.
    tone = str(order.get("tone", "spicy")).lower().split()[0]
    intensity = LEGACY_TONE_MAP.get(tone, "spicy")
    return {
        "pet": {"name": order.get("pet_name", "Buster")},
        "target": {
            "name": order.get("recipient_name", "James"),
            "relationship": order.get("relationship", "owner"),
        },
        "facts": list(order.get("roast_facts", [])),
        "intensity": intensity,
    }


def _trim(words: str, n: int) -> str:
    parts = words.split()
    return " ".join(parts[:n]) + ("..." if len(parts) > n else "")


def build_roast_json(norder: dict, templates: dict[str, list[str]],
                     fact_start: int = 0) -> dict:
    """Build canonical roast.json from a normalized order.

    templates is the per-style joke architecture (owned by generate.py
    in V1; a model scorer replaces it later without changing this contract).
    fact_start rotates the fact window — "more personal" rerolls use
    later facts so Take 2 mines new material instead of repeating Take 1.
    """
    pet = norder["pet"]["name"]
    target = norder["target"]["name"]
    window = norder["facts"][fact_start:fact_start + 3] or norder["facts"][:3]
    facts = window  # V1: three bits. More facts → later bits/packs.
    style = INTENSITY_MAP[norder["intensity"]]
    arch = templates.get(style, templates["savage"])

    bits = []
    for i, fact in enumerate(facts):
        fact = fact.strip()
        Fact = fact[0].upper() + fact[1:] if fact else fact
        text = arch[i % len(arch)].format(fact=fact, Fact=Fact,
                                          recipient=target, pet=pet)
        # Split "setup. punchline" on the template's natural seam: first
        # sentence is setup, remainder is punchline.
        parts = [p.strip() for p in text.split(". ") if p.strip()]
        setup = parts[0] + ("" if parts[0].endswith(".") else ".")
        punch = ". ".join(parts[1:]) if len(parts) > 1 else setup
        bits.append({
            "setup": setup,
            "punchline": punch,
            "reaction": REACTIONS[i % len(REACTIONS)],
        })
    while len(bits) < 1:
        bits.append({"setup": f"{target} walked in.", "punchline": "The crowd went mild.",
                     "reaction": "reaction_shot"})

    strongest = f"{bits[-1]['setup']} {bits[-1]['punchline']}".strip()
    first_setup = bits[0]["setup"].rstrip(".")
    first_setup = first_setup[0].upper() + first_setup[1:] if first_setup else first_setup
    return {
        "headline": strongest,
        "opening": f"{target}. My {norder['target']['relationship']}.",
        "bits": bits,
        "callback": f"Remember {first_setup}? Still true.",
        "signoff": "",  # filled by caller from order signoff
        "card_line": _trim(strongest, 12),
        "visual": {"pet": pet.lower(), "stage": STAGE},
    }
