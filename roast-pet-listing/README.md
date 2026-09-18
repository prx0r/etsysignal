# roast-pet-listing — one visual engine

All Etsy listing media renders from `src/pet.json`. New customer? Export a new pet.json, re-render, done.

```bash
# from etsysignal/
python -m roastpet.remotion output/<slug>/   # refresh src/pet.json

cd roast-pet-listing
npm install
npm run still:hero        # 2000x2000 Etsy hero
npm run render:listing    # 15s silent listing video (Etsy strips audio anyway)
npm run render:vertical   # 9:16 TikTok/Reels cut
```

Compositions: `Hero`, `ListingVideo` (CardReveal), `VerticalAd` (PhoneDemo), `HowItWorks`, `Reroll`.

Layout zones for `Hero` must match `output/<slug>/listing/thumbs/A_spec.json`.
