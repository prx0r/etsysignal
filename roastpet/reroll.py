#!/usr/bin/env python3
"""roastpet reroll — Directed regeneration with pairwise preservation.

Usage:
    python -m roastpet.reroll <take1_slug> <direction> --order <order_dir>

Directions: funnier | meaner | cuter | deadpan | trailer

Never overwrites Take 1. Writes Take 2 as a new bundle + takes.json
pairwise record: {take1, take2, direction, kept: null}.

The kept field is filled in when the customer picks a winner.
A vs B → kept is the training signal.
"""
import json
import sys
from pathlib import Path

from .generate import run_pipeline, REROLL_DIRECTIONS

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "output"


def reroll(take1_slug: str, direction: str, order_dir: str) -> dict:
    direction = direction.lower()
    if direction not in REROLL_DIRECTIONS:
        raise ValueError(f"Unknown direction {direction!r}. Choose from {sorted(REROLL_DIRECTIONS)}")

    take1_dir = OUT_DIR / take1_slug
    if not take1_dir.exists():
        raise FileNotFoundError(f"No Take 1 bundle at {take1_dir}")

    print(f"=== REROLL: {direction} ===")
    print(f"  Take 1: {take1_slug} (preserved, never overwritten)")
    print()

    # Take 2 is a full fresh pipeline run — new slug, new audio, new avatar.
    manifest = run_pipeline(order_dir, reroll_style=direction)
    take2_slug = manifest["slug"]

    pair = {
        "take1": take1_slug,
        "take2": take2_slug,
        "direction": direction,
        "style_take1": json.load(open(take1_dir / "pipeline_manifest.json")).get("style"),
        "style_take2": manifest["style"],
        "kept": None,
        "note": "Customer picks a winner. A vs B → kept is the training signal.",
    }
    pair_path = OUT_DIR / take2_slug / "takes.json"
    pair_path.write_text(json.dumps(pair, indent=2))
    # Also drop a pointer in Take 1 so the studio can list both.
    (take1_dir / f"reroll_{direction}_{take2_slug}.json").write_text(json.dumps(pair, indent=2))

    print("=== REROLL COMPLETE ===")
    print(f"  Take 1: output/{take1_slug}/  (original)")
    print(f"  Take 2: output/{take2_slug}/  ({direction})")
    print(f"  Pair:   output/{take2_slug}/takes.json")
    return pair


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="roastpet directed reroll")
    parser.add_argument("take1_slug", help="Existing Take 1 bundle slug in output/")
    parser.add_argument("direction", help="funnier | meaner | cuter | deadpan | trailer")
    parser.add_argument("--order", required=True, help="Order directory (must contain order.json)")
    args = parser.parse_args()
    reroll(args.take1_slug, args.direction, args.order)
