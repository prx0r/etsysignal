# DEV.md — Pet Roast MVP Build Plan

## Core Principle

**Do not rebuild what FreakTown already has.**

FreakTown already has:
- Structured comedy beats
- Exact pause timing
- TTS caching
- Performance profiles
- 3D avatar creation/fallbacks
- Lipsync animation
- Stage playback
- Captions
- Share pages
- Persistent bundles

## The One New Thing: `gift_roast.py`

### Input
Realistic fake Etsy order:
- 3 pet photos
- Recipient name + age + occasion
- 5 funny facts
- Pet personality
- Optional birthday message

### Process
```
RoastOrder
    ↓
roast writer (new)
    ↓
structured beats (75-110 words)
    ↓
_save_bundle() (existing)
    ↓
set.wav + timing (existing)
    ↓
real pet photo → portrait.png (new: copy + resize)
    ↓
existing /api/avatar (existing)
    ↓
existing Three.js stage (existing)
    ↓
/gift/<slug> (new: gift presentation mode)
```

### Output
45-second vertical video: pet roasts recipient, wishes happy birthday.

## What Already Works

- `_save_bundle()` = product compiler
- `/api/avatar` = portrait → GLB pipeline
- Stage playback with captions
- Voice performance
- Beat-to-expression mapping

## What's New

1. `RoastOrder` schema (fake Etsy order)
2. Roast writer (structured beats, not prose)
3. Gift presentation mode (`/gift/<slug>`)
4. Screen-record export to MP4

## Build Order

1. Create demo order (buster-001)
2. Write roast compiler
3. Map to FreakTown beats
4. Create gift presentation page
5. Screen-record one perfect demo
