"""Gift Page — create /gift/<slug> in FreakTown."""
import json
import os
from pathlib import Path

FREAK_DIR = Path("/home/ubuntu/freaktown/freaks")


def create_gift_page(slug: str) -> dict:
    """Create gift presentation page for a Freak bundle."""
    bdir = FREAK_DIR / slug
    
    if not bdir.exists():
        return {"ok": False, "error": "bundle not found"}
    
    # Read bundle data
    character = json.loads((bdir / "character.json").read_text())
    meta = json.loads((bdir / "meta.json").read_text())
    
    # Create gift page data
    gift_data = {
        "slug": slug,
        "pet_name": character.get("name", "Pet"),
        "premise": character.get("premise", ""),
        "duration": meta.get("duration_s", 0),
        "words": meta.get("word_count", 0),
        "status": "ready",
    }
    
    # Save gift data
    (bdir / "gift.json").write_text(json.dumps(gift_data, indent=2))
    
    return {
        "ok": True,
        "slug": slug,
        "gift_url": f"/gift/{slug}",
        "pet_name": character.get("name", "Pet"),
    }


if __name__ == "__main__":
    slug = "buster-68ad29"
    result = create_gift_page(slug)
    print(json.dumps(result, indent=2))
