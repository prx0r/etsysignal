"""Photo QC — validate pet photos before avatar generation."""
import json
from pathlib import Path

UPLOAD_DIR = Path(__file__).parent / "roastpet_checkpoint1_demo" / "02_customer_uploads" / "buster-001" / "raw"


def check_photo_quality(image_path: str) -> dict:
    """Check if a photo meets minimum quality requirements."""
    issues = []
    
    # Check file exists
    if not Path(image_path).exists():
        return {"ok": False, "issues": ["file_not_found"]}
    
    # Check file size (too small = low res)
    size = Path(image_path).stat().st_size
    if size < 10000:  # < 10KB
        issues.append("low_resolution")
    
    # Check if it's actually an image
    try:
        with open(image_path, "rb") as f:
            header = f.read(4)
            if header[:2] != b'\xff\xd8' and header[:4] != b'\x89PNG':
                issues.append("not_image")
    except:
        issues.append("unreadable")
    
    return {
        "ok": len(issues) == 0,
        "issues": issues,
        "size_bytes": size,
    }


def validate_order_photos(order_dir: str) -> dict:
    """Validate all photos in an order."""
    raw_dir = Path(order_dir) / "raw"
    if not raw_dir.exists():
        raw_dir = Path(order_dir)
    
    photos = list(raw_dir.glob("pet-*.png")) + list(raw_dir.glob("pet-*.jpg"))
    
    results = []
    for photo in sorted(photos):
        result = check_photo_quality(photo)
        result["filename"] = photo.name
        results.append(result)
        print(f"  {photo.name}: {'OK' if result['ok'] else 'FAIL - ' + ', '.join(result['issues'])}")
    
    # Check minimum requirements
    ok_count = sum(1 for r in results if r["ok"])
    has_front = any("front" in r["filename"].lower() or "01" in r["filename"] for r in results)
    has_body = any("body" in r["filename"].lower() or "02" in r["filename"] for r in results)
    
    verdict = "PASS" if ok_count >= 3 and has_front else "NEEDS_REPLACEMENT"
    
    return {
        "verdict": verdict,
        "total_photos": len(photos),
        "ok_photos": ok_count,
        "has_front_face": has_front,
        "has_full_body": has_body,
        "results": results,
    }


if __name__ == "__main__":
    order_dir = Path(__file__).parent / "roastpet_checkpoint1_demo" / "02_customer_uploads" / "buster-001"
    result = validate_order_photos(order_dir)
    print(json.dumps(result, indent=2))
