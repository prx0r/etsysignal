# recon.md — Full File Audit: Gold References from etsysignal + freaktown

> Every reusable file, what it does, and exactly how to wire it into the roast.pet pipeline.
> 2026-09-18

---

## SECTION A: THE PIPELINE (etsysignal)

These are the files we own that define the roast.pet product flow.

### A1. `roast/gift_roast.py` — Main Entry Point
- **What it does:** Loads an order directory, compiles comedy beats, saves a FreakTown bundle
- **Imports from freaktown:** `from app import _save_bundle`
- **Hardcoded path bug:** `sys.path.insert(0, "/home/ubuntu/freaktown")` — must fix
- **How to use:** This becomes `roastpet/generate.py` — the thing Etsy webhook triggers after purchase
- **Input:** `roast/demo_orders/buster-001/order.json` + pet photos
- **Output:** A freaktown bundle at `freaks/buster-001/`

### A2. `roast/pipeline.py` — Full Pipeline (Alternative Entry)
- **What it does:** order → beats → FreakTown bundle → copy pet photos → gift page URL
- **Overlaps with gift_roast.py** — contains duplicate `compile_beats()` logic
- **How to use:** Merge the useful parts (photo copying, gift page URL) into A1, discard the rest

### A3. `roast/roast_compiler.py` — Standalone Beat Compiler
- **What it does:** Turns RoastOrder JSON into structured comedy beats WITHOUT needing FreakTown
- **How to use:** This is the "comedy engine" adapter — takes Etsy order data and produces the beat script that FreakTown's delivery sequencer will render
- **Key function:** Loads `order.json`, produces beat list with text/type/pause

### A4. `roast/demo_orders/buster-001/order.json` — Demo Order
- **What it does:** Canonical test input — pet name "Buster", owner "James", occasion "50th birthday"
- **How to use:** The reference input for the full flow. Every pipeline change gets tested against this.

### A5. `roastpet_checkpoint1_demo/` — Checkpoint Fixture
- **What it does:** Rigorous end-to-end test fixture with 8 quality-graded pet photos, pipeline contracts, QA acceptance criteria, and edge cases
- **How to use:** The acceptance test suite. Run the pipeline, check outputs against contracts in `04_pipeline_contracts/`.

### A6. `data/` — Market Research
- **Files:** `ETSY_ANALYSIS.md`, `SALES_DATA.md`, `COMPETITOR_ANALYSIS.md`
- **How to use:** Reference for Etsy listing copy, pricing, SEO keywords. Not code.

### A7. `strats/` — Strategy Documents
- **Key file:** `strats/ETSY_PLAN.md` — canonical plan with 3 launch SKUs, pricing, 5-question listing design
- **How to use:** Source of truth for product decisions. When in doubt, check this first.

---

## SECTION B: COMEDY ENGINE (freaktown)

These are the freaktown files that do the actual creative work.

### B1. `app.py:642` — `_save_bundle(data)` ⭐ CRITICAL
- **What it does:** The central persistence function. Creates a complete character bundle:
  - Generates slug from character name + hash
  - Writes `character.json` (name, species, premise, vibe, voice)
  - Writes `delivery.json` (full beat-by-beat performance spec)
  - Composes `set.wav` (TTS each beat, insert exact silence, produce final audio)
  - Writes `offsets.json` (measured beat timings)
  - Generates `walkout.wav` (procedural music)
  - Writes `walkout.json` (genre/mood/energy/seed)
  - Copies portrait, writes `visual.json`
  - Writes `meta.json` (slug, status, lineage)
  - Builds BASIC 3D avatar body
- **How to use:** This is the single function we call to produce a pet's show. Feed it a character dict with pet photos, voice, and delivery beats.

### B2. `app.py:122` — `detect_beats(text)` ⭐
- **What it does:** Splits flat comedy text into structured beats with type (setup/escalation/punchline/closer), pause duration, and stage direction
- **How to use:** Feed the roast compiler's output through this to get表演-ready beats

### B3. `app.py:38` — `tts_generate(text, voice, pace)` ⭐
- **What it does:** Generate speech WAV from text using edge-tts (free, no API key)
- **How to use:** The voice engine. Each beat gets synthesized through this.

### B4. `app.py:95` — `compose_beats(beat_audios, sr)` ⭐
- **What it does:** Compose speech chunks with exact silence gaps into final WAV
- **How to use:** After TTS generates each beat, this assembles them into the final roast audio

### B5. `app.py:1009` — `WALKOUT_GENRES`
- **What it does:** Dict mapping genre names to instrument descriptions and BPMs (funk, rock, electronic, jazz, orchestral, comedy, hip-hop, disco)
- **How to use:** Each pet gets a walkout genre. Map pet personality/vibe to genre.

### B6. `app.py:1191` — `FREAK_SPECIES`
- **What it does:** List of species names for random character generation (moth, pigeon, roomba, dog, toaster, goblin, etc.)
- **How to use:** Add pet species: "dachshund", "labrador", "persian_cat", "hamster", etc.

### B7. `app.py:1199` — `FREAK_VOICES`
- **What it does:** Dict mapping vibe strings to edge-tts voice IDs
- **How to use:** Pet voice selection — map roast intensity/comedy style to voice presets

### B8. `app.py:1220` — `_roll_character(locks)`
- **What it does:** Rolls a complete random character with voice and walkout recipe
- **How to use:** Template for how to build a pet character dict from order data

---

## SECTION C: DELIVERY SYSTEM (freaktown)

The TTS-to-timed-audio pipeline.

### C1. `backend/services/delivery/sequencer.py:47` — `DeliveryBeat` ⭐
- **What it does:** Dataclass for a single beat: text, timing, delivery params, stage direction
- **How to use:** Each roast line becomes a DeliveryBeat

### C2. `backend/services/delivery/sequencer.py:66` — `DeliveryScore` ⭐
- **What it does:** Full delivery spec: provider, voice, and list of DeliveryBeats
- **How to use:** The roast compiler produces a DeliveryScore that the sequencer renders

### C3. `backend/services/delivery/sequencer.py:116` — `arrange(text)` ⭐
- **What it does:** Splits flat text into DeliveryBeats with conservative timing defaults
- **How to use:** Quick path — feed raw roast text, get timed beats out

### C4. `backend/services/delivery/sequencer.py:228` — `compose(score)` ⭐
- **What it does:** Render a DeliveryScore into final WAV: TTS each beat, insert exact silence, encode
- **How to use:** The production renderer. Takes DeliveryScore → produces set.wav

---

## SECTION D: COMEDY GENERATION + SCORING (freaktown)

### D1. `scripts/comedy_generator.py:104` — `ComedyGenerator` ⭐
- **What it does:** Evolutionary set writer: generate → score → mutate losers → keep winners
- **Key method:** `evolve_set(topic, max_attempts)` at line 155
- **How to use:** Retrain on pet roast topics instead of stand-up comedy. Feed it pet names, owner facts, roast intensity.

### D2. `scripts/comedy_generator.py:206` — `ComedyGenerator.run(target)`
- **What it does:** Full evolutionary loop across multiple topics
- **How to use:** Generate a batch of roast scripts, keep only the ones that score well

### D3. `scripts/comedy_scorer.py:191` — `ComedyScorer` ⭐
- **What it does:** ML model: sentence embeddings + hand features → predicted comedy score
- **How to use:** Retrain on pet roast acceptance data (reroll vs keep signals)

### D4. `scripts/comedy_scorer.py:36` — `extract_features(text)`
- **What it does:** Hand-crafted features: word count, sentiment, punctuation patterns
- **How to use:** Feature extraction for the scorer. Add pet-specific features.

---

## SECTION E: SCORING RUBRIC (freaktown)

### E1. `backend/services/scoring/rubric.py:71` — `RubricScorer` ⭐
- **What it does:** LLM-as-Judge: 5-dimension rubric (opening_hook, escalation, specificity, closer, voice) with few-shot gold anchors from Kill Tony
- **How to use:** Swap Kill Tony anchors for pet roast gold examples. This judges whether a roast is funny.

### E2. `backend/services/ella/judge.py` — `EllaJudgeAccumulator`
- **What it does:** Real-time beat-by-beat scoring with laugh-curve features
- **Score bands:** 0-3 disaster, 3-5 cut, 5-7 survive, 7-8.5 strong, 8.5+ exceptional
- **How to use:** Live scoring during generation — kill bad roasts before they reach the customer

---

## SECTION F: MUSIC + SOUND (freaktown)

### F1. `sound_synth.py:19` — `GENRES` ⭐
- **What it does:** Dict mapping genre names to BPM, bass patterns, wave types, drum kits, lead lines
- **How to use:** Each pet's walkout theme is generated from a genre recipe

### F2. `sound_synth.py:183` — `generate(recipe, seed)` ⭐
- **What it does:** Main synth: deterministic walkout WAV from genre/mood/energy/shape
- **How to use:** Free, instant, no GPU. Every pet gets a unique procedural theme.

### F3. `sound_bank.py:27` — `SOUNDS` ⭐
- **What it does:** Catalog of 25+ comedy SFX: rimshot, laugh, clap, boo, crickets, gasp, fanfare, sad trombone, suspense, walkout stings
- **How to use:** Dog audience reactions, band stings, host walkout — all in here

### F4. `sound_bank.py:170` — `SoundBank`
- **What it does:** Manager for pre-generated comedy sounds: generate, cache, play, list
- **How to use:** Asset manager for the show's sound effects

---

## SECTION G: CHARACTER SYSTEM (freaktown)

### G1. `basic_body.py:37` — `SPECIES` ⭐
- **What it does:** Dict mapping species to body proportions, palette, hat/glasses probabilities (8 species: human, 2 dogs, 2 robots, 2 objects, pigeon, goblin, shadow)
- **How to use:** Add "dachshund", "labrador", "cat", "hamster", "corgi" with appropriate proportions

### G2. `basic_body.py:117` — `build(species, name, seed)` ⭐
- **What it does:** Build a rigged GLB body with skeleton + jawOpen morph target
- **How to use:** Every pet gets an instant $0 3D body. No external service needed.

### G3. `face_profiles.py:52` — `POG_FACE_V1`
- **What it does:** Tuple of 26 semantic face intent names (jaw_open, visemes, blinks, smiles, etc.)
- **How to use:** Universal face language. Maps any avatar format to our intent system.

### G4. `face_profiles.py:87` — `EXPRESSION_INTENTS`
- **What it does:** Maps expression words (neutral, happy, sad, angry, surprised, deadpan, annoyed, smirk) to POG_FACE_V1 intent weights
- **How to use:** Pet facial expressions during the roast — deadpan delivery, shocked reaction, smug grin

### G5. `comedians.py` — Character Templates ⭐
- **What it does:** 5 starter comedians with full minute scripts, voices, vibes
  - No-Nose Nolan (sniffer dog) — line 6
  - Corporate Robot — line 39
  - World's Oldest Roomba — line 72
  - Conspiracy Pigeon — line 108
  - Medieval LinkedIn Knight — line 142
- **How to use:** Template format for building pet character dicts. Each has: name, species, premise, vibe, voice, set (array of lines)

### G6. `house_guests.py` — 14 Celebrity Characters
- **What it does:** ChatGPT, Alexa, Siri, C-3PO, R2-D2, HAL, GLaDOS, Bender, Marvin, Data, Clippy, Wheatley, HK-47, Kryten
- **How to use:** Reference for character voice/premise/vibe structure. Also potential "guest appearances" in pet shows.

---

## SECTION H: PERFORMANCE + MOTION (freaktown)

### H1. `backend/services/performance_compiler.py:153` — `compile_performance()` ⭐
- **What it does:** Full pipeline: text + voice → PerformancePlan with audio, segments, cues
- **How to use:** The production path from roast script to playable performance

### H2. `backend/services/motion_compiler.py:178` — `MotionCompiler`
- **What it does:** Resolves semantic directions to concrete timed motion cues (gestures, expressions, camera cuts, SFX)
- **How to use:** Camera grammar for the late-night show — "host leans in", "cut to audience", "close-up on pet"

### H3. `backend/services/clips/planner.py:206` — `plan_package()` ⭐
- **What it does:** Auto-generates content package: YouTube full set, TikTok 9:16, best-20s clip, best-40s clip, score reveal, thumbnail, captions SRT
- **How to use:** Every roast automatically gets social-ready clips for sharing

### H4. `backend/services/clips/planner.py:100` — `find_best_window()`
- **What it does:** Sliding window to find peak-laugh-density time ranges
- **How to use:** Auto-select the funniest 15-second clip for the Etsy listing video

---

## SECTION I: SHOW RUNTIME (freaktown)

### I1. `runtime.py:77` — `Show` ⭐
- **What it does:** Full show state machine: acts, phases, timestamps, laugh tracking
- **How to use:** The Late Late Dog Show IS a Show instance. Host intro → pet performs → audience reacts → host follow-up → next roast.

### I2. `runtime.py:31` — `Act`
- **What it does:** One comedian's performance slot with audience metrics
- **How to use:** Each roast segment is an Act

### I3. `show.py:147` — `run_show()` ⭐
- **What it does:** CLI episode runner: Ella intro → acts → judging → interviews → outro
- **How to use:** Template for the full show flow. Swap Ella for "Dog Host", swap comedians for pet guests.

### I4. `ella.py:21` — `SYSTEM_PROMPT`
- **What it does:** Host personality definition: speaking style, stage powers, verdict format
- **How to use:** Adapt for the Late Late Dog Show host character

### I5. `ella.py:179` — `Ella.judge_set()`
- **What it does:** Host reacts to a set with one observation + verdict
- **How to use:** Host follow-up after each pet roast

---

## SECTION J: RENDERING (freaktown)

### J1. `renderers.py:118` — `perform(character, audio_sha, duration_ms, quality, allow_paid)`
- **What it does:** Route one performance: choose renderer, return render plan
- **How to use:** The renderer router — picks cheapest capable renderer at requested quality

### J2. `renderers.py:90` — `choose(manifest, quality, allow_paid)`
- **What it does:** Pick cheapest capable renderer
- **How to use:** Map pet order to visual renderer (BASIC for free, Runway for premium)

### J3. `tts.py:13` — `synthesize(text, voice, filename)` ⭐
- **What it does:** Generate speech via edge-tts, returns MP3 path
- **How to use:** Free TTS fallback

### J4. `tts_provider.py:244` — `get_provider(name)`
- **What it does:** Provider factory: edge/kokoro/qwen/magic
- **How to use:** Switch TTS providers per quality tier

---

## SECTION K: PARTY MODE (freaktown)

### K1. `party.py:392` — `_rr_create(room)` / `party.py:400` — `_rr_start_round()`
- **What it does:** Roast Relay: collect lines from players, vote on best, TTS assembles
- **How to use:** Audience participation mode — "Write a roast for Biscuit"

### K2. `party.py:462` — `_rr_reveal(room)`
- **What it does:** Reveal assembled roast, switch to voting, trigger TTS
- **How to use:** The "reveal" moment in interactive roast modes

---

## SECTION L: SCHEMAS + CONTRACTS (freaktown)

### L1. `contracts/` — JSON Schemas
- **Files:** character.json, delivery.json, avatar.json, events.json, format.json, lineage.json, offsets.json, performance.json
- **How to use:** API contracts between pipeline stages. Build against these, not ad-hoc dicts.

### L2. `schemas/` — Pack Schemas
- **Files:** character pack schema, delivery v1 schema
- **How to use:** Validate that our pet character bundles conform to FreakTown's expected format

---

## SECTION M: STAGE + WEB (freaktown)

### M1. `stage/` — Three.js Stage Renderer
- **Files:** app.js, index.html, style.css
- **What it does:** Browser-based 3D stage with camera presets (WIDE, MEDIUM, CLOSE, SIDE)
- **How to use:** The visual stage for the late-night show. CameraDirector handles cuts.

### M2. `packages/stage-runtime/` — TypeScript Runtime
- **Key files:** StageRenderer.ts, AudioBus.ts, CameraDirector.ts, LipSync.ts, Transport.ts
- **How to use:** The browser-side rendering engine. Handles lip sync, camera cuts, audio playback.

---

## SECTION N: DEMO ASSETS (etsysignal)

### N1. `roastpet_checkpoint1_demo/02_customer_uploads/buster-001/raw/` — Pet Photos
- **pet_01_front_face.png** (500K) — Primary identity reference. Sharp, well-lit.
- **pet_02_full_body.png** (740K) — Avatar geometry/pose reference.
- **pet_03_side_threequarter.png** (617K) — Body proportions.
- **pet_04_motion_blur.png** (406K) — Personality/style only.
- **pet_05_low_resolution.png** (356K) — Edge case: degrade gracefully.
- **pet_06_overexposed.png** (417K) — Edge case: recover or warn.
- **pet_07_tight_crop.png** (793K) — FAIL_GEOMETRY.
- **pet_08_blurry.png** (188K) — FAIL_IDENTITY.

### N2. `roast/demo_orders/buster-001/` — Demo Order + Photos
- **order.json** — Canonical test input (Buster, James, 50th birthday)
- **pet-1.jpg** (26K) — Three sleeping Yorkies
- **pet-2.jpg** (27K) — Two golden retriever puppies
- **pet-3.jpg** (28K) — Adult golden retriever

### N3. `roastpet_checkpoint1_demo/04_pipeline_contracts/` — Stage Contracts
- **intake_contract.json** — What the intake validator must produce
- **avatar_contract.json** — What the avatar generator must produce
- **pog_identity_contract.json** — What the persistent identity system must produce

### N4. `roastpet_checkpoint1_demo/05_card/` — Card Contract
- **card_product_contract.json** — Prodigi 5x7 card spec (330gsm, comedy club layout)
- **CARD_COPY_FIXTURE.txt** — Front/inside/back copy

### N5. `roastpet_checkpoint1_demo/07_video/` — Video Contract
- **performance_contract.json** — 9:16, 30-60s, 1080x1920

---

## THE WIREFRAME: How to Connect Everything

```
ETSY ORDER (order.json + photos)
        │
        ▼
┌─────────────────────────┐
│ INTAKE (A3 + N3)        │
│ roast_compiler.py       │
│ parse order → beats     │
│ validate photos (N1)    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ COMEDY ENGINE (D1 + D4) │
│ comedy_generator.py     │
│ pet facts → roast lines │
│ ComedyScorer filters    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ BEAT DETECTION (B2)     │
│ app.py:detect_beats()   │
│ roast text → beats      │
│ with types + pauses     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ CHARACTER BUILD (G1+G2) │
│ basic_body.build()      │
│ pet species → 3D body   │
│ voice assignment (B7)   │
│ walkout genre (F1+F2)   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ DELIVERY (C1-C4)        │
│ sequencer.py            │
│ DeliveryScore → WAV     │
│ TTS (B3+B4)             │
│ set.wav + offsets.json  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ BUNDLE (B1)             │
│ _save_bundle()          │
│ Full character bundle:  │
│ character.json          │
│ delivery.json           │
│ set.wav                 │
│ walkout.wav             │
│ portrait.png            │
│ avatar.glb              │
│ meta.json               │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ SHOW RUNTIME (I1-I3)    │
│ Show state machine      │
│ Host intro → roast →    │
│ audience → follow-up →  │
│ next roast → outro      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ CLIPS (H3 + H4)        │
│ planner.py              │
│ Auto-generate:          │
│ - Full 9:16 video       │
│ - TikTok 9:16 clip      │
│ - Best-15s for Etsy     │
│ - SRT captions          │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ CARD (N4)               │
│ Prodigi API             │
│ Render card art         │
│ Generate QR → URL       │
│ Submit print order      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ DELIVERY                │
│ Customer gets:          │
│ - Physical card (Prodigi)│
│ - roast.pet/biscuit link│
│ - 1 free reroll         │
│ - Access to studio      │
└─────────────────────────┘
```

---

## PRIORITY: Files to Touch First

1. **`app.py:642`** `_save_bundle` — the single function that produces everything
2. **`app.py:122`** `detect_beats` — turns text into表演ready beats
3. **`app.py:38`** `tts_generate` — free TTS engine
4. **`sound_synth.py:183`** `generate` — procedural walkout music
5. **`basic_body.py:117`** `build` — instant 3D pet body
6. **`backend/services/delivery/sequencer.py:116`** `arrange` — text → timed beats
7. **`backend/services/delivery/sequencer.py:228`** `compose` — beats → WAV
8. **`roast/roast_compiler.py`** — order → roast beats (adapter layer)
9. **`roast/demo_orders/buster-001/order.json`** — test input
10. **`roastpet_checkpoint1_demo/04_pipeline_contracts/`** — acceptance contracts
