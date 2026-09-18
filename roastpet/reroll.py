#!/usr/bin/env python3
"""roastpet reroll — V1 directed regeneration with pairwise preservation.

Usage:
    python -m roastpet.reroll <take1_slug> <reason> --order <order_dir> [--note TEXT]

V1 reasons (northstar.md — "What should Biscuit change?"):
    funnier | meaner | gentler | more personal | different voice | something else

  funnier / meaner / gentler → new style, same facts.
  more personal              → same style, later facts (new material).
  different voice            → same roast, next voice in the cycle.
  something else             → same style regen + free-text note recorded.

Never overwrites Take 1. Writes Take 2 + takes.json:
  {take1, take2, reason, note, kept: null}.
"""
import json
import sys
from pathlib import Path

from .comedy import normalize_order
from .generate import run_pipeline, REROLL_DIRECTIONS, VOICE_CYCLE

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "output"


def reroll(take1_slug: str, reason: str, order_dir: str, note: str = None) -> dict:
    reason = reason.lower()
    if reason not in REROLL_DIRECTIONS:
        raise ValueError(f"Unknown reason {reason!r}. Choose from {sorted(REROLL_DIRECTIONS)}")
    if reason == "something else" and not note:
        raise ValueError("'something else' needs --note TEXT so we know what to change")

    take1_dir = OUT_DIR / take1_slug
    if not take1_dir.exists():
        raise FileNotFoundError(f"No Take 1 bundle at {take1_dir}")
    take1 = json.loads((take1_dir / "pipeline_manifest.json").read_text())

    kwargs: dict = {"reroll_style": reason}
    if reason == "more personal":
        kwargs["fact_start"] = 3  # mine later facts, don't repeat Take 1
    if reason == "different voice":
        try:
            nxt = VOICE_CYCLE[(VOICE_CYCLE.index(take1["voice"]) + 1) % len(VOICE_CYCLE)]
        except ValueError:
            nxt = VOICE_CYCLE[0]
        kwargs["voice_override"] = nxt
    if note:
        kwargs["note"] = note

    print(f"=== REROLL: {reason} ===")
    print(f"  Take 1: {take1_slug} ({take1.get('style')}, preserved)")
    if note:
        print(f"  Note: {note}")
    print()

    manifest = run_pipeline(order_dir, **kwargs)
    take2_slug = manifest["slug"]

    pair = {
        "take1": take1_slug,
        "take2": take2_slug,
        "reason": reason,
        "note": note,
        "style_take1": take1.get("style"),
        "style_take2": manifest["style"],
        "voice_take1": take1.get("voice"),
        "voice_take2": manifest.get("voice"),
        "kept": None,
        "note2": "Customer picks a winner. A vs B → kept is the training signal.",
    }
    (OUT_DIR / take2_slug / "takes.json").write_text(json.dumps(pair, indent=2))
    (take1_dir / f"reroll_{reason.replace(' ', '_')}_{take2_slug}.json").write_text(
        json.dumps(pair, indent=2))

    print("=== REROLL COMPLETE ===")
    print(f"  Take 1: output/{take1_slug}/  (original)")
    print(f"  Take 2: output/{take2_slug}/  ({reason})")
    return pair


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="roastpet V1 directed reroll")
    parser.add_argument("take1_slug", help="Existing Take 1 bundle slug in output/")
    parser.add_argument("reason", help="funnier | meaner | gentler | more personal | different voice | something else")
    parser.add_argument("--order", required=True, help="Order directory (must contain order.json)")
    parser.add_argument("--note", default=None, help="Free text for 'something else'")
    args = parser.parse_args()
    reroll(args.take1_slug, args.reason, args.order, args.note)
