"""Photo Pipeline — pet photo -> FreakTown portrait."""
import json
import shutil
from pathlib import Path

FREAK_DIR = Path("/home/ubuntu/freaktown/freaks")


def process_pet_photos(order_dir: str, slug: str) -> dict:
    """Process pet photos for FreakTown bundle."""
    raw_dir = Path(order_dir) / "raw"
    bdir = FREAK_DIR / slug
    
    # Find best photo (front face preferred)
    best_photo = None
    for f in ["pet_01_front_face.png", "pet_02_full_body.png", "pet_03_side_threequarter.png"]:
        src = raw_dir / f
        if src.exists():
            best_photo = src
            break
    
    if not best_photo:
        return {"ok": False, "error": "no_pet_photo"}
    
    # Copy as portrait.png
    dst = bdir / "portrait.png"
    shutil.copy(best_photo, dst)
    
    # Get image info
    size = dst.stat().st_size
    
    return {
        "ok": True,
        "source": best_photo.name,
        "destination": str(dst),
        "size_bytes": size,
        "slug": slug,
    }


if __name__ == "__main__":
    order_dir = "roastpet_checkpoint1_demo/02_customer_uploads/buster-001"
    slug = "buster-68ad29"
    result = process_pet_photos(order_dir, slug)
    print(json.dumps(result, indent=2))
