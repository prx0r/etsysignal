"""Etsy Snapshot — capture shop/listing metrics from Etsy API."""
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode

API_KEY = os.environ.get("ETSY_API_KEY", "")
SHARED_SECRET = os.environ.get("ETSY_SHARED_SECRET", "")

def etsy_get(path, params=None):
    url = f"https://openapi.etsy.com/v3/application{path}"
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={"x-api-key": f"{API_KEY}:{SHARED_SECRET}"})
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}

def snapshot_listings(keywords=None, limit=20):
    if not keywords:
        keywords = ["personalized football video gift"]
    listings = []
    for kw in keywords:
        data = etsy_get("/listings/active", {
            "keywords": kw, "limit": min(limit, 100),
            "fields": "listing_id,title,price,num_favorers,tags,url,views,shop_id"
        })
        if "results" in data:
            for r in data["results"]:
                listings.append({
                    "keyword": kw,
                    "listing_id": r["listing_id"],
                    "title": r["title"][:80],
                    "price": r["price"]["amount"] / r["price"]["divisor"],
                    "favorites": r.get("num_favorers", 0),
                    "views": r.get("views", 0),
                })
    return listings

if __name__ == "__main__":
    keywords = sys.argv[1:] if len(sys.argv) > 1 else None
    listings = snapshot_listings(keywords)
    print(json.dumps(listings, indent=2))
