# roast.pet Strategy & Advice Report

> Timestamped capture of strategic decisions, product direction, and technical insights.
> Generated: 2026-09-18

---

## 1. The Core Insight: Show Format, Not Talking-Pet Video

**Decision: "The Late Late Dog Show" is the format.**

The current Etsy market is overwhelmingly "send photo → pet talks/dances → receive MP4." There are 139+ "AI dog video" results and 283+ custom pet birthday video results, including established sellers doing talking-dog invitations.

**Our differentiation is format/IP, not AI quality.**

The product is:

> **Your Pet Goes on a Late-Night Show and Roasts You**

That's an Etsy thumbnail/title someone understands instantly.

### Why This Works

- **90% of creative work is reusable.** One studio, one host, one audience, one camera grammar, one set of transitions and reaction shots. Each order changes the guest pet, voice, jokes and details.
- **Much more economical** than generating an entirely novel film every time.
- **Immediately more memorable** than the current Etsy market.
- **The barking audience is exactly the kind of stupid detail we'd obsess over.** The moat starts becoming a library of genuinely funny reusable comedy machinery.

### The Show Structure (Mostly Fixed)

```
0–3s     ANNOUNCER
         "Tonight on The Late Late Dog Show..."

3–6s     DOG ENTERS
         barking/applause + band

6–10s    HOST
         "So, Biscuit, tell us about Tom."

10–20s   PET ROAST #1
         → dog audience erupts

20–25s   HOST FOLLOW-UP

25–35s   PET ROAST #2
         → cutaway to shocked Chihuahua

35–40s   CALLBACK / KILLER LINE

40–45s   THEME + personalized end card
         "Happy Birthday, Tom"
```

### The Moat: Comedy Machinery Library

The moat becomes a library of genuinely funny reusable comedy machinery:

- Dog audience reactions
- Host archetypes
- Bands
- Intros
- Camera cuts
- Hecklers
- Running jokes
- Visual gags
- Interview structures
- Roast structures

**This is basically Freaktown rescued as an Etsy-funded comedy laboratory.** Every purchased pet gives us another character and every accept/reroll tells us which comedy machinery worked.

---

## 2. Don't Sell an AI Video Generator — Sell a Persistent Character

**Decision: The product is a persistent comedy character, not a one-shot video.**

The Etsy purchase isn't:

> £15 → 40-second AI video

It's:

> £15 → Biscuit now exists as a comedy character.

The video is just Biscuit's first episode.

### The roast.pet Studio

After receiving the initial video:

**Biscuit's Dressing Room**
`Tonight's appearance ✓`

Then:

**Bring Biscuit Back On**
- Roast Dad
- Roast Mum
- Roast Me Again
- Talk About the Cat
- Birthday Special
- Christmas Special
- Breaking News
- Ask Biscuit a Question

This is where the persistent pet identity becomes valuable.

### Existing Competition Validates This

- One talking-pet seller charges ~$35 for a 10–20 second clip with unlimited revisions
- A recent pet-band seller sells 30-second personalized performances with multiple reference photos/roles
- 376+ custom pet-song results on Etsy
- Roughly $10–20 gets a 10–20 second talking-pet clip with voice style and custom dialogue

**All of them are essentially:** `inputs → seller generates asset → MP4/MP3 → done`

**Our thing becomes:** `inputs → persistent comedy character → physical gift + evolving digital experience`

---

## 3. Rerolls as a Product Mechanic + Training Data

**Decision: Make rerolls part of the product, structured to solve customer satisfaction AND train roast.pet simultaneously.**

### The Feedback Loop

```
Upload pet
   ↓
Choose:
• Roast level
• Voice
• Show style
• Occasion
   ↓
Generate
   ↓
┌─────────────────────────────┐
│     BAXTER'S ROAST          │
│          ▶ PLAY             │
│                             │
│  LOVE IT                    │
│                             │
│  TRY ANOTHER                │
│  ├─ Funnier                 │
│  ├─ Meaner                  │
│  ├─ Cuter                   │
│  ├─ Different voice         │
│  └─ Different show style    │
└─────────────────────────────┘
```

Give **one free directed reroll** with every purchase. Not simply "regenerate." Force a tiny feedback signal:

> What should we change?

Every unhappy generation becomes labelled preference data:

`generation A → "not funny enough" → generation B → accepted`

This is enormously more useful than a star rating.

### Premium = 3 Candidates, Not Unlimited

- **Basic — £9.99:** roast.pet character + one generated show + **1 free reroll**
- **Studio — £14.99:** generate **3 different performances**, customer selects winner + one refinement
- **Premium — £24.99:** physical card + character + three performances + premium visual/avatar treatment + intro theme

Etsy's personalization system supports up to five typed questions and optional paid personalization add-ons. This structure maps unusually well onto Etsy.

**Important: keep the transaction on Etsy.** Etsy's policy prohibits moving an Etsy-initiated transaction off-platform. roast.pet is the creation/consumption surface, not an attempt to dodge Etsy checkout.

### Preserve the Original

Don't overwrite generation #1. After a reroll:

```
BAXTER'S STUDIO

TAKE 1                    TAKE 2
▶                          ▶
"Original"                "Meaner"

                         ★ KEEP THIS
```

Now the user has made an actual pairwise preference judgment: **A vs B → B**

That's much higher-quality training/optimization data than thumbs-up/down.

Eventually: `pet features + occasion + recipient relationship + humour preference + joke architecture + voice + visual style + duration → acceptance`

Then optimize the generation policy from actual human choices.

---

## 4. Etsy as the Distribution + Checkout Layer

**Decision: Make Etsy the acquisition + checkout layer, and roast.pet the experience after purchase.**

### Etsy Listing Design

**"Personalized Pet Roast Card + Your Pet's Comedy Show"**

Buyer supplies:
1. **Pet photos** — Etsy file upload (up to 10 images/files)
2. **Pet name + funny facts** — text
3. **Comedy style** — dropdown: Gentle / Savage / Unhinged / Deadpan
4. **Occasion** — Birthday / Gotcha Day / Christmas / Just Because
5. **Show style** — Stand-up / News Report / Documentary / Talk Show / Music Intro

Etsy supports those input types natively with up to five customization fields.

### Etsy Listing Video Strategy

Etsy listing videos are only 3–15 seconds and Etsy strips their audio. You can have two per listing.

**Don't waste dialogue there.** Make a completely visual 10–15 second transformation:

`normal dog photo → curtain opens → dog walks onto late-night set → dog host interviews it → dog audience goes insane → owner gets roasted → "YOUR PET. THEIR OWN SHOW."`

Big subtitles carry the joke because Etsy removes audio.

Images can explain: **PHOTO → PERSONALIZED SHOW → WATCH/SHARE → FREE REROLL**

Etsy recommends showing finished personalized examples rather than a generic placeholder as the main image.

### Etsy-Native Upsell Structure

Etsy personalization fields can have add-on pricing, and Etsy shows the increased price before checkout:

```
Pet Roast Card                     £9.99

Comedy style:
○ Gentle
● Savage
○ Unhinged

Add:
□ Digital talking-pet video        +£5
□ Original intro theme             +£4
□ 3 extra roast scenes             +£6
□ T-shirt                          +£15
□ Mug                              +£12
```

Every customer gets the roast.pet profile regardless.

---

## 5. The Physical Card as Killer SKU

**Decision: The physical card is a physical access token to the character.**

Front:

> **HAPPY BIRTHDAY FROM THE ONLY MEMBER OF THIS FAMILY WITH STANDARDS**

Pet photo.

Inside:

> Biscuit has prepared some remarks.

**Tap/scan → roast.pet/biscuit**

And Biscuit launches into the personalized routine.

Then beneath it:

**Make Biscuit say something else →**

That's qualitatively different from QR-linking an MP4.

---

## 6. The First Product — Brutally Specific

**Decision: Don't launch 20 mediocre formats. Launch one.**

> **Personalized Pet Roast — Your Dog Goes on a Late-Night Show**

Not "AI pet studio." Not "Pog." Not ten formats.

### What the buyer supplies:

- 3–5 photos
- Owner name
- Three funny facts
- Roast intensity

### What they get:

```
ETSY
  ↓
pet photo
name
3 funny facts
roast intensity
occasion
  ↓
ROAST.PET
  ↓
┌────────────────────────────┐
│       BISCUIT              │
│                            │
│        [ pet ]             │
│                            │
│  "Professional freeloader" │
│                            │
│   ▶ WATCH MY ROAST         │
│                            │
│  🎤 Another Roast          │
│  🎵 My Theme Song          │
│  📺 Breaking News          │
│  💬 Make Me Say...         │
└────────────────────────────┘
```

**Don't build a complicated editor yet.** The first "studio" should be five big buttons plus maybe one text box. The generative machinery underneath can be sophisticated; the consumer UI shouldn't be.

### The First Milestone

> Produce three genuinely excellent fake customer episodes, create the Etsy listing, and get the first paid stranger.

No dashboard. No elaborate studio. No Pogtown architecture. Once someone pays, fulfil partly manually if necessary and learn exactly what they care about.

---

## 7. Renderer as an Experimental Variable

**Decision: Don't commit to one visual model. Make renderer an experimental variable.**

```
PET PROFILE
name / images / personality / joke context
                │
          COMEDY ENGINE
                │
      script + voice + music
                │
       RENDERER ROUTER
       /      |       \
      /       |        \
Runway    Higgsfield   cheap image→video
 Avatar     style       pipeline
      \       |        /
       \      |       /
          CUSTOMER
             ↓
      accept / reroll
             ↓
        RESULT DATA
```

Acceptance rate becomes the objective function:

- `Runway avatar + deadpan → 67% first-pass acceptance`
- `cinematic pet + dramatic announcer → 81%`
- `talk-show pet + custom intro → 91%`

Runway recommends testing cheaper generations first before escalating to higher-cost Gen-4 generation.

### Onboarding: Don't Ask for AI Terminology

Ask:

**"What kind of show should your pet star in?"**

- 🎤 Stand-up comedian
- 📺 Breaking-news anchor
- 🎬 Hollywood documentary
- 🎵 Music superstar
- 🎙️ Late-night guest

roast.pet determines renderer, prompt, voice, intro and composition. Later experimentally add/remove styles based on conversion + acceptance.

---

## 8. Voice: Fictional, Not Cloned

**Decision: Don't emphasize human voice cloning initially. Make the pet's fictional voice using voice design.**

ElevenLabs can generate several voice previews from a textual voice description and let us select one.

The studio could have:

**Biscuit's voice**

`[ Tiny aristocrat ] [ Cockney geezer ] [ Movie trailer ] [ Exhausted dad ]`

Generate four previews → buyer taps one → that's Biscuit's persistent voice.

Pet fictional voice avoids consent mess (ElevenLabs requires verification for Professional Voice Clones, can't create from someone else's recording) and is funnier anyway.

---

## 9. Frontiers to Exploit

### ElevenLabs Music v2.5
- Structured composition plans + improved output
- Every pet gets a procedural intro theme

### Higgsfield
- **Seed Audio**: dialogue + sound effects + music/ambience together
- **Genjutsu/Motion Transfer**: transfer funny human-performed comedy motions onto pet characters (accepts source video + up to 30 reference photos, outputs up to 1080p)
- Much closer to a scalable comedy production system than generating random text-to-video every order

### Runway
- Character/avatar video generation via API
- Persistent avatars with appearance, voice, personality

---

## 10. The Data Moat Loop

```
Funny product → delighted customer → review → Etsy distribution → more customers → comedy preference data → funnier product
```

Etsy's search ranking is affected by conversion/engagement and customer experience. Strong reviews build buyer confidence.

Every order generates:
- Another pet identity
- Another comedy preference signal
- Another generated joke
- Another video
- Another reaction/regeneration signal

Eventually roast.pet learns:

> dachshund + deadpan + owner embarrassment + 8-second setup + dramatic news music → extremely shareable.

**That's the Freaktown/Pogtown comedy-learning system we wanted, except customers are paying us to populate and test it.**

---

## 11. Version Roadmap

| Version | Description |
|---------|-------------|
| **v0** | Etsy fulfilment engine — generate the show from Etsy order |
| **v1** | Customer reroll studio — directed regeneration with feedback |
| **v2** | Persistent pet characters — Biscuit exists as a reusable identity |
| **v3** | Conversational creation — "make Dad's birthday episode savage" |
| **v4** | Live interactive dog talk show (Gemini/Jev-style) |
| **v5** | Pogtown: characters interacting with each other live |

**None of v1–v5 deserves attention until strangers buy v0.**

---

## 12. What We Already Have (Reused from Freaktown)

### Directly Reusable

| Asset | Location | Notes |
|-------|----------|-------|
| Comedy generation pipeline | `scripts/comedy_generator.py` | Evolutionary LLM writing + ML evaluation. Retrain on pet roast data |
| 5-dimension rubric | `backend/services/scoring/rubric.py` | Few-shot gold anchors. Swap Kill Tony for pet roast examples |
| Ella M judge system | `ella.py` | Host personality + interview + verdict. Adapt for pet roast context |
| Real-time beat scoring | `EllaJudgeAccumulator` | Laugh-curve features, 5 dimensions |
| Delivery sequencer | `backend/services/delivery/sequencer.py` | Complete TTS-to-timed-audio pipeline |
| Beat detection | `app.py detect_beats()` | Punchline/tag/closer classification + pause timing |
| Procedural walkout music | `sound_synth.py` | 8 genres, deterministic, instant, free |
| Sound bank | `sound_bank.py` | 25+ comedy SFX templates |
| Clip planner | `backend/services/clips/planner.py` | TikTok/YouTube/social clips with laugh-window detection |
| Party mode | `party.py` Roast Relay | Players write roast lines, vote, TTS assembles |
| Bundle format | `freaks/<slug>/` | Portable, complete. Any new character drops in |
| BASIC body generator | `basic_body.py` | Instant $0 rigged GLB bodies for 16 species. Add "cat", "hamster" |
| Face profiles | `face_profiles.py` | Morph detection + POG_FACE_V1 semantic intents |
| Character catalogs | 5 starters + 14 house guests | Full scripts, voices, performance profiles |
| Vibe profiles | 7 performance profiles | Character personality → stage behavior parameters |
| Schemas/contracts | `contracts/` | Stable interfaces: character, delivery, avatar, performance |

### Adaptable (Minor Modification)

- `show.py` CLI runner — swap comedian list for pet characters
- `app.py` character rolling — add pet species to `FREAK_SPECIES`
- `party.py` words list — replace with pet-themed words
- `backend/services/freaktown/bundle.py` SPECIES_MAP — add pet species
- `comedy_generator.py` TOPICS — replace with pet roast topics
- Walkout genre-mood mappings — add pet species → genre mappings

---

## 13. Demo Assets Available

### From `roastpet_checkpoint1_demo/`

**8 PNG images of Buster the dachshund** — same dog, different quality/role:

| File | Quality | Use |
|------|---------|-----|
| `pet_01_front_face.png` (500K) | Sharp, well-lit | Primary identity reference |
| `pet_02_full_body.png` (740K) | Full body on lawn | Avatar geometry/pose reference |
| `pet_03_side_threequarter.png` (617K) | Three-quarter view | Body proportions |
| `pet_04_motion_blur.png` (406K) | Motion blur | "Personality" shot (style only) |
| `pet_05_low_resolution.png` (356K) | Low-res | Edge case: degrade gracefully |
| `pet_06_overexposed.png` (417K) | Washed out | Edge case: recover or warn |
| `pet_07_tight_crop.png` (793K) | Face-only crop | FAIL_GEOMETRY |
| `pet_08_blurry.png` (188K) | Heavily blurred | FAIL_IDENTITY |

**Additional demo order photos** (different dogs):
- `pet-1.jpg` — Three sleeping Yorkies (multiple pet edge case)
- `pet-2.jpg` — Two golden retriever puppies
- `pet-3.jpg` — Adult golden retriever

**No video, GIF, or animation files exist.** Only JSON contracts describe expected outputs.

### From `freaktown/`

- 19 ready-made characters with full scripts
- 8 procedural walkout music genres
- 25+ comedy SFX templates
- Default VRM avatar
- Full Three.js stage renderer with camera presets

---

## 14. What to Build First

### Step 1: The Demo Pack
Create three genuinely excellent fake customer episodes using existing assets:
- Buster the dachshund (already have 8 quality-graded photos)
- Show format: The Late Late Dog Show
- Use Freaktown's comedy pipeline + delivery sequencer + procedural music

### Step 2: The Etsy Listing
- Listing title: "Personalized Pet Roast — Your Dog Goes on a Late-Night Show"
- 3–15 second listing video (visual only, big subtitles)
- Main image: finished personalized example (not generic placeholder)
- 5 personalization fields matching the spec above

### Step 3: First Paid Stranger
- Fulfil manually if necessary
- Learn exactly what they care about
- Record every signal: acceptance, reroll reasons, timing, engagement

---

## 15. Key Quotes to Remember

> "That is a show format, not just a talking-pet video."

> "£15 → Biscuit now exists as a comedy character. The video is just Biscuit's first episode."

> "The card is a physical access token to the character."

> "Don't sell an AI video generator. Sell the customer a hilarious persistent version of their pet."

> "Park the giant live Pogtown vision. Use Etsy to earn the right to build it."

> "Funny product → delighted customer → review → Etsy distribution → more customers → comedy preference data → funnier product."

> "None of v1–v5 deserves attention until strangers buy v0."

> "Acceptance rate becomes the objective function."

> "That's basically Freaktown rescued as an Etsy-funded comedy laboratory."

> "Every purchased pet gives us another character and every accept/reroll tells us which comedy machinery worked."
