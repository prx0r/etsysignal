# roast-pet-listing — one visual engine

All Etsy listing media renders from `src/pet.json`. New customer? Export a new pet.json, re-render, done.

```bash
# from etsysignal/
python -m roastpet.remotion output/<slug>/   # refresh src/pet.json

cd roast-pet-listing
npm install
npm run still:hero        # 2000x2000 Etsy hero
npm run render:listing    # V1 explain video (silent — Etsy strips audio anyway)
npm run render:supercut   # V2 comedy supercut (silent)
npm run render:vertical   # 9:16 TikTok/Reels cut
```

Compositions: `Hero`, `ListingVideo` (CardReveal), `Supercut`, `VerticalAd` (PhoneDemo), `HowItWorks`, `Reroll`.

`src/pet.json` is exported from the bundle's `roast.json` (`python -m roastpet.remotion output/<slug>/`) — renderers consume roast.json, never raw orders.

Layout zones for `Hero` must match `output/<slug>/listing/thumbs/A_spec.json`.
