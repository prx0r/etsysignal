# FLOW_REPORT — Full demo-pack flow, end to end

> Timestamped: 2026-09-18 ~01:40 UTC
> Order: `roast/demo_orders/buster-001/` (Buster the dachshund roasts James for his 50th)
> Goal hardcoded per brief: Late Late Dog Show → bundle → card → listing → thumbnails → video.

---

## 1. What ran (all green, first pass unless noted)

| Stage | Command | Result |
|-------|---------|--------|
| Pipeline Take 1 | `python -m roastpet.generate roast/demo_orders/buster-001/` | `output/buster-e83ad4/` — 13 beats, 169 words, **95.9s**, voice en-GB-ThomasNeural (savage) |
| Intake QC | `python -m roastpet.intake roastpet_checkpoint1_demo/02_customer_uploads/buster-001/` | **8/8 verdicts match** the fixture manifest; roles map front/full/side/favourite correctly |
| Reroll Take 2 | `python -m roastpet.reroll buster-e83ad4 cuter --order roast/demo_orders/buster-001/` | `output/buster-ac3326/` — 13 beats, 172 words, **84.8s**, voice en-AU-WilliamNeural (gentle). Take 1 untouched, `takes.json` with `kept: null` |
| Card files | `python -m roastpet.cards output/<slug>/` (both takes) | `card/` ×7 files each. Front: **JAMES IS 50. / BUSTER HAS NOTES.** — fixture voice exact |
| Listing pack | `python -m roastpet.listing output/<slug>/` (both takes) | title, description, 5-question personalization.json, savage_map, 13 tags, 10-shot shotlist |
| Thumbnails | `python -m roastpet.thumbnails output/buster-e83ad4/` | A/B/C specs + 2000px mocks + 150px Etsy-size shrinks |
| Remotion engine | `roast-pet-listing/` scaffold + `python -m roastpet.remotion output/buster-e83ad4/` | 5 compositions, `pet.json` exported from bundle, all imports resolve |
| Video storyboard | `python -m roastpet.video output/<slug>/` (both takes) | 6-shot 15s silent board, subtitles capped at 8 words |

---

## 2. Verification numbers

- **Audio:** `set.wav` 4.6MB (Take 1) / 4.0MB (Take 2); offsets sum to duration within rounding (95,880ms ↔ 95.9s).
- **Delivery:** `freaktown.delivery.v1`, edge-tts, 13 offsets, walkout `rock/menacing/high` procedural 8s.
- **Avatar:** `avatar.glb` 11KB rigged BASIC body + `avatar.json` (auto-built by `_save_bundle`).
- **Photos:** 3/3 customer photos copied into each bundle.
- **Pairwise:** Take 1 savage vs Take 2 gentle — different joke architecture, voices, affection lines; `takes.json` awaiting customer `kept`.
- **Remotion:** `pet.json` valid; Hero/CardReveal/PhoneDemo/HowItWorks/Reroll imports resolve.

---

## 3. Known deviations / debt

1. **Duration 85-96s vs 30-60s video contract.** The 13-beat Late Late Dog Show structure (announcer + host ×2 + opener + premise + 5 roasts + affection + follow-up + signoff) overshoots `07_video/performance_contract.json`. Options: cut to 3 roast facts for v0, or split into Part 1/Part 2. Not fixed yet — needs a product call.
2. **No real hero art yet.** Thumbnails are compositional wireframes (zones + 150px legibility proven at block level). Final A/B/C renders need the image-gen pass in `roast-pet-listing` (cardFront/showFrame props are stubbed).
3. **Remotion not `npm install`ed.** Scaffold + compositions are written and import-checked, but nothing has rendered until assets exist. Deliberate — no point rendering wireframes.
4. **`gift_roast.py` / `pipeline.py` still exist** with duplicate `compile_beats()`. `roastpet/generate.py` supersedes them; old files should be deleted or archived after sign-off.
5. **Hardcoded `/home/ubuntu/freaktown` path** persists (now in one place: `roastpet/generate.py`). Env-var next.
6. **freaktown bundles are the source of truth at runtime** (`freaks/<slug>/`); `output/` is a detached copy. The `card/` + `listing/` + `takes.json` files written to `output/` after the run are NOT mirrored back into `freaks/`. Decide: either write everything into `freaks/` directly or treat `output/` as canonical.

---

## 4. File map (new this session)

```
roastpet/
  generate.py    order → beats → _save_bundle → photos → card_spec → manifest
  intake.py      photo QC vs checkpoint fixture (8/8)
  reroll.py      directed reroll + takes.json pairwise record
  cards.py       Prodigi Fine Art 5x7 production files + QR payload
  listing.py     Etsy title/description/personalization/tags/shotlist
  thumbnails.py  A/B/C hero specs + mocks + 150px shrinks
  remotion.py    bundle → roast-pet-listing/src/pet.json
  video.py       15s silent storyboard (8-word subtitle cap)

roast-pet-listing/
  package.json, remotion.config.ts, README.md
  src/index.ts, src/Root.tsx, src/pet.json
  src/compositions/Hero, CardReveal, PhoneDemo, HowItWorks, Reroll, types

output/
  buster-e83ad4/  Take 1 (savage) — bundle + card + listing + thumbs + video board
  buster-ac3326/  Take 2 (gentle) — bundle + card + listing + video board + takes.json
```

Also this session: `advice.md`, `recon.md`, `cardplan.md` (strategy docs, repo root).
