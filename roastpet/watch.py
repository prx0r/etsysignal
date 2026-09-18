#!/usr/bin/env python3
"""roastpet watch — Static roast.pet/r/:id page stub per bundle.

Usage:
    python -m roastpet.watch output/<slug>/

V1 (northstar.md): barely a website. Mobile-first: title, player,
WATCH THE ROAST, reroll section. QR points at roast.pet/r/<slug>;
this file is the static artifact that page serves until the real
backend exists. Audio-only player for now (set.wav); the MP4 show
render replaces the <audio> tag without changing anything else.
"""
import html
import json
import sys
from pathlib import Path

REASONS = ["Funnier", "Meaner", "Gentler", "More personal",
           "Different voice", "Something else"]


def build_watch(bundle_dir: str) -> Path:
    bdir = Path(bundle_dir)
    manifest = json.loads((bdir / "pipeline_manifest.json").read_text())
    roast = manifest.get("roast", {})
    slug = manifest["slug"]
    pet = html.escape(roast.get("visual", {}).get("pet", "buster").upper())
    target = html.escape((manifest.get("normalized_order", {})
                          .get("target", {}).get("name", "James")).upper())
    card_line = html.escape(roast.get("card_line", ""))
    takes_path = bdir / "takes.json"
    takes = json.loads(takes_path.read_text()) if takes_path.exists() else None

    takes_html = ""
    if takes:
        takes_html = f"""
    <h2>TAKE 1 / TAKE 2</h2>
    <p>Reason: {html.escape(takes.get('reason', ''))}. Pick a winner:</p>
    <p><a href="../{html.escape(takes['take1'])}/watch.html">▶ TAKE 1 ({html.escape(str(takes.get('style_take1', '')))})</a></p>
    <p><a href="watch.html">▶ TAKE 2 ({html.escape(str(takes.get('style_take2', '')))})</a></p>"""

    reasons_html = "\n".join(
        f"      <li>{r}</li>" for r in REASONS)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{pet} ROASTS {target} — roast.pet</title>
<style>
  body {{ background:#14141E; color:#FFF; font-family:system-ui,sans-serif;
         max-width:560px; margin:0 auto; padding:24px 16px 64px; text-align:center; }}
  .brand {{ color:#FFDC78; letter-spacing:4px; font-size:14px; }}
  h1 {{ font-size:40px; margin:8px 0; }}
  .line {{ font-size:20px; color:#FFDC78; }}
  audio {{ width:100%; margin:24px 0; }}
  .reroll {{ border-top:1px solid #333; margin-top:32px; padding-top:24px; }}
  ul {{ list-style:none; padding:0; }}
  li {{ background:#222; margin:8px 0; padding:12px; border-radius:8px; }}
  a {{ color:#FFDC78; }}
</style>
</head>
<body>
  <div class="brand">ROAST.PET</div>
  <h1>{pet}<br>ROASTS {target}</h1>
  <p class="line">“{card_line}”</p>
  <audio controls src="set.wav"></audio>
  <p>WATCH THE ROAST</p>
  {takes_html}
  <div class="reroll">
    <h2>Didn't nail it?</h2>
    <p>↻ Request one reroll — what should {pet} change?</p>
    <ul>
{reasons_html}
    </ul>
  </div>
</body>
</html>
"""
    out = bdir / "watch.html"
    out.write_text(page)
    print(f"=== WATCH: {slug} ===")
    print(f"  {out} (roast.pet/r/{slug})")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m roastpet.watch output/<slug>/")
        sys.exit(1)
    build_watch(sys.argv[1])
