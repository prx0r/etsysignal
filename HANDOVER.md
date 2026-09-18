# Handover — etsysignal

## What This Repo Is

**roast.pet** — Personalized pet comedy gift for Etsy.

Upload pet → tell gossip → pet roasts someone → physical card + digital show.

## What Works

### Pipeline (tested end-to-end)
```bash
python3 roast/pipeline.py roast/demo_orders/buster-001/
```
Order → Beats → FreakTown bundle → Portrait → Gift URL

### Components
- `roast/gift_roast.py` — orchestrates roast generation
- `roast/pipeline.py` — full pipeline
- `roast/photo_qc.py` — photo quality validation
- `roast/photo_pipeline.py` — pet photo → portrait
- `roast/roast_compiler.py` — order → FreakTown beats
- `roast/gift_page.py` — gift page creation
- `roast/card_art.py` — card artwork generation

### Demo Assets
- `roast/roastpet_checkpoint1_demo/` — 8 real pet images
- `roast/demo_orders/buster-001/order.json` — fake Etsy order

## What's NOT Done Yet

1. Photo QC needs real image validation (Pillow)
2. Card artwork needs actual rendering
3. QR code generation
4. Prodigi PDF for printing
5. Video export (screen-record for now)
6. ElevenLabs voice design
7. Reroll/feedback loop
8. Etsy listing copy

## Key Architecture

- **Roast.pet** = storefront (Etsy)
- **Pog** = persistent pet character
- **Pog.pet** = character home
- **FreakTown** = performance engine (backend)

## How to Continue

1. Add real pet photos to demo order
2. Fix photo QC with Pillow
3. Create card artwork with QR
4. Screen-record /gift/<slug> for demo video
5. Build Prodigi PDF
6. Create Etsy listing

## Dependencies

- FreakTown (at /home/ubuntu/freaktown)
- Pillow (for image processing)
- Prodigi API (for printing)
