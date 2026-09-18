# FLOW_REPORT — V1 end-to-end (northstar.md build)

> Timestamped: 2026-09-18 ~02:10 UTC
> Order: `roast/demo_orders/buster-001/` (Buster roasts James, 50th)
> Spec: `northstar.md` — one SKU, one podium, one roast, one scan.

---

## 1. What ran

| Stage | Command | Result |
|-------|---------|--------|
| Pipeline Take 1 | `python -m roastpet.generate roast/demo_orders/buster-001/` | `output/buster-ff41e5/` — 7 beats, 73 words, **48.1s**, savage |
| Card | `python -m roastpet.cards output/buster-ff41e5/` | V1 copy: ROAST.PET PRESENTS / card_line teaser / TONIGHT'S ROASTER / WATCH YOUR ROAST / `roast.pet/r/<slug>` QR |
| Listing | `python -m roastpet.listing output/buster-ff41e5/` | 4 questions, intensity map, 13 tags, 8-image + 2-video shotlist |
| Thumbs | `python -m roastpet.thumbnails output/buster-ff41e5/` | A/B/C podium-grammar specs + 2000px mocks + 150px shrinks |
| Remotion export | `python -m roastpet.remotion output/buster-ff41e5/` | `pet.json` from roast.json (canonical consumer proven) |
| Storyboard | `python -m roastpet.video output/buster-ff41e5/` | 6-shot 15s silent Explain board, 8-word subtitle cap |
| Watch page | `python -m roastpet.watch output/buster-ff41e5/` | `watch.html` — roast.pet/r/buster-ff41e5 stub |
| Reroll Take 2 | `python -m roastpet.reroll buster-ff41e5 "more personal" --order ...` | `output/buster-3cb709/` — 6 beats, 62 words, **40.2s**, new material (facts 4-5), Take 1 untouched |
| Take 2 downstream | cards + listing + video + watch on Take 2 | complete, own QR per slug |

---

## 2. Verification numbers

- **Durations 48.1s / 40.2s** — inside the 30-60s video contract (V0 debt closed by the 7-beat podium grammar).
- **roast.json** in both bundles: headline/opening/bits[3|2]/callback/signoff/card_line/visual{pet, roast_v1}.
- **Pairwise:** savage/savage, different facts, `takes.json` reason=`more personal`, `kept: null`.
- **Intake QC:** 8/8 vs fixture manifest (unchanged, still passing).
- **Remotion:** 6 compositions (Hero, ListingVideo, Supercut, VerticalAd, HowItWorks, Reroll), all imports resolve.
- **Card QR:** `https://roast.pet/r/<slug>` — matches watch-page route.

---

## 3. V1 deltas from the previous build

- Late Late Dog Show grammar (13 beats, host, 85-96s) → podium grammar (7 beats, no host, 40-48s).
- 5 personalization fields → 4 (photos / who / dirt / Playful-Spiricy-Savage).
- Reroll directions (funnier/meaner/cuter) → 6 V1 reasons incl. more personal (fact rotation), different voice (voice cycle), something else (recorded note).
- Card copy → northstar V1 voice; QR route → `/r/:id`.
- New modules: `comedy.py` (roast.json engine), `watch.py` (static page stub).
- Old V0 output dirs (`buster-e83ad4`, `buster-ac3326`) deleted; V1 dirs are the tree now.

## 4. Known debt

1. Final hero art still needs the image-gen pass (wireframes only; `cardFront`/`showFrame` props stubbed).
2. Remotion never `npm install`ed — deliberate until art exists.
3. `gift_roast.py` / `pipeline.py` still present, superseded by `roastpet/generate.py` — delete after sign-off.
4. Hardcoded `/home/ubuntu/freaktown` in one place (`generate.py`) — env-var next.
5. `output/` vs `freaks/` canonical-store question still open.
6. Manual fulfilment per spec — no Prodigi automation (correct for V1).
