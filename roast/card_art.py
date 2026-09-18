"""Card Art — generate card artwork with QR code."""
import json
from pathlib import Path

FREAK_DIR = Path("/home/ubuntu/freaktown/freaks")


def generate_card_art(slug: str) -> dict:
    """Generate card artwork for a Freak bundle."""
    bdir = FREAK_DIR / slug
    
    if not bdir.exists():
        return {"ok": False, "error": "bundle not found"}
    
    character = json.loads((bdir / "character.json").read_text())
    meta = json.loads((bdir / "meta.json").read_text())
    
    # Card layout (5x7 inches = 152x178mm)
    card = {
        "slug": slug,
        "front": {
            "layout": "5x7",
            "pet_name": character.get("name", "Pet"),
            "tagline": f"YOUR PET HAS SOMETHING TO SAY",
            "portrait": f"/freaks/{slug}/portrait.png",
        },
        "inside_left": {
            "joke": "A joke from the roast",
            "branding": "roast.pet",
        },
        "inside_right": {
            "message": "Happy Birthday!",
            "qr_url": f"roast.pet/{slug}",
            "cta": "SCAN TO WATCH YOUR PET ROAST THEM",
        },
        "back": {
            "branding": "Made alive by roast.pet",
        },
    }
    
    # Save card spec
    (bdir / "card.json").write_text(json.dumps(card, indent=2))
    
    return {
        "ok": True,
        "slug": slug,
        "card_spec": card,
    }


if __name__ == "__main__":
    slug = "buster-68ad29"
    result = generate_card_art(slug)
    print(json.dumps(result, indent=2))
