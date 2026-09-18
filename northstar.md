# NORTHSTAR — roast.pet V1

> Saved: 2026-09-18. The canonical product spec. Everything else grows outward from this exact object later; none of it contaminates launch.

**V1 collapses back to one SKU and one joke mechanic.**

## V1 product

**One thing:**

> **Personalized Pet Roast Birthday Card — Watch Your Pet Roast You**

No studio. No selectable show formats. No music video. No T-shirts. No persistent chat.

The canonical artifact is:

```text
                    PHYSICAL CARD

             ┌──────────────────────┐
             │      THE ROAST       │
             │                      │
             │        🐕            │
             │      BISCUIT         │
             │    at the podium     │
             │                      │
             │  TOM HAS THE SOCIAL  │
             │  SKILLS OF A LAMP.   │
             └──────────────────────┘
                       │
                       │ scan
                       ▼
                   roast.pet
                       │
                       ▼
             THE ACTUAL ROAST
```

Think the visual grammar of a celebrity roast: dark stage, spotlight, microphone/podium, audience, giant **ROAST** identity. But **do not copy Netflix/Comedy Central branding, logos, set designs, typography or trade dress**. Build roast.pet's own recognizable roast-stage IP.

The pet at the podium should become the canonical roast.pet image.

---

## Exact buyer experience

Exactly four personalization fields initially:

**1. `Pet photos` — required upload**

Allow 3–5 photos, even though Etsy technically supports up to 10.

Instruction:

`Upload 3–5 clear photos showing your pet's face and body.`

**2. `Who are we roasting?` — required text**

`Name + relationship to pet. Example: James, Biscuit's dad.`

**3. `Give us the dirt` — required text**

This is the valuable input.

`Tell us 3–5 funny facts, habits or embarrassing stories about them.`

Allow plenty of characters.

**4. `Roast level` — dropdown**

`Playful / Spicy / Savage`

That's it.

Don't ask the customer to write jokes. **They supply facts; roast.pet supplies comedy.**

---

## What gets generated

The order becomes one structured object:

```json
{
  "pet": {
    "name": "Biscuit",
    "photos": ["..."]
  },
  "target": {
    "name": "James",
    "relationship": "owner"
  },
  "facts": [
    "spends 40 minutes doing his hair",
    "Biscuit sleeps in his bed",
    "always loses his keys",
    "claims he's starting the gym Monday"
  ],
  "intensity": "spicy"
}
```

Generation produces **two outputs from the same comedy package**.

### A. Card

High-resolution canonical portrait:

```text
ROAST.PET PRESENTS

      [ BISCUIT ]
     behind podium
       microphone
       spotlight

"JAMES SPENDS 40 MINUTES
 ON HIS HAIR JUST TO LOOK
 LIKE THAT."

       THE ROAST
```

The card joke should be **one killer line**, not the entire roast. The physical card becomes the teaser.

### B. Roast video

30–60 seconds. Same Biscuit. Same stage. Same visual identity.

```text
0:00  Roast.pet sting

0:02  "James. My owner."

0:05  setup #1
      punchline
      DOG AUDIENCE BARKS

0:13  setup #2
      punchline
      reaction shot

0:22  callback

0:28  strongest joke

0:34  dog audience loses it

0:38  "Happy birthday, James."

0:41  roast.pet
```

The barking audience is now **part of the brand grammar**.

Every order uses essentially the same set/camera/reaction library. Vary the pet and material, not an entire cinematic universe every time.

---

## The physical card

Prodigi Fine Art Greeting Cards, 5×7", 324gsm, 300dpi source artwork. Production 24–72 hours, worldwide shipping from UK/EU fulfilment, wholesale from ~£0.75 before tax/shipping. Personalization inside and outside, Etsy fulfilment supported.

**Front:** Biscuit roast podium portrait + killer headline.

**Inside left:** another still / `TONIGHT'S ROASTER: BISCUIT`.

**Inside right:**

> Biscuit has more to say.

Large QR.

> **WATCH YOUR ROAST**

Birthday message beneath.

**Back:** tiny roast.pet mark.

Don't automate Prodigi on day one. Fulfil the first few manually. Automate once orders happen. (Prodigi has both Etsy integration and a print API — no architectural dead end.)

---

## roast.pet V1 (the website)

Barely a website. QR resolves to `roast.pet/r/7K2P9D`. Mobile page:

```text
┌────────────────────────┐
│       roast.pet        │
│                        │
│        BISCUIT         │
│     ROASTS JAMES       │
│                        │
│   ┌────────────────┐   │
│   │                │   │
│   │     ▶          │   │
│   │                │   │
│   └────────────────┘   │
│                        │
│     WATCH THE ROAST    │
│                        │
│  Didn't nail it?       │
│  ↻ Request one reroll  │
│                        │
└────────────────────────┘
```

**Don't build AR for V1.** Marketing can say "scan the card and it comes alive," but technologically QR → beautiful full-screen video is 95% of the magic for ~5% of the work. Call it **"Scan to watch"**, not AR, until it genuinely is AR.

---

## The reroll is part of V1

One free reroll. Not a blank complaint box — ask:

**What should Biscuit change?**

* Funnier
* Meaner
* Gentler
* More personal
* Different voice
* Something else

Preserve both versions. `TAKE 1 / TAKE 2 → KEEP THIS ONE`. Store the choice.

First genuine data flywheel: `inputs → jokes → render → rejection reason → reroll → customer preference`. Eventually more valuable than the generator itself.

---

## Etsy listing architecture

### Image 1 — THE THUMBNAIL

No process diagram. One insanely good finished card. Square master ~2000×2000+.

```text
              premium gift scene

      ╭──────────────────────╮
      │     THE ROAST        │
      │                      │
      │       BISCUIT        │
      │       🐕 🎙          │
      │                      │
      │ "JAMES HAS NEVER     │
      │  WON AN ARGUMENT     │
      │  WITH A DOG."        │
      ╰──────────────────────╯

              envelope

        phone partly visible
     showing SAME DOG on stage
```

**The product itself explains the joke.** Primary image must show a finished personalized item, not a blank template. Biscuit / James is the canonical fake example.

### Images 2–8

2. **The magic** — YOUR PET ROASTS YOU. `Upload pet → Receive card → Scan → Watch roast`
3. **Video screenshot** — phone fullscreen, Biscuit at podium, subtitle + dog audience
4. **Personalization** — YOU GIVE US THE DIRT. YOUR PET DOES THE REST.
5. **Physical card** — front / inside / back. A real printed card arrives.
6. **Free reroll** — Includes one free reroll. Take 1 / Take 2.
7. **Gifting** — recipient scanning card / laughing.
8. **Examples** — cat, Labrador, dachshund. Same roast stage. Not just dogs.

### TWO listing videos (3–15s each, no audio)

**Video 1 — explain product:** pet photo → roast card → QR scan → Biscuit on roast stage → recipient laughing. Large burned-in captions.

**Video 2 — sell the comedy:** rapid supercut. BISCUIT ROASTS JAMES cut MABEL ROASTS MUM cut GARY ROASTS DAD, dog audience insane. End: YOUR PET. YOUR ROAST. Creative A/B surface.

---

## Implementation architecture

```text
ETSY ORDER
    │
    ├── photos
    ├── target
    ├── dirt
    └── intensity
           │
           ▼
      ORDER INGEST
           │
           ▼
     COMEDY ENGINE
           │
       structured
       roast.json
       /       \
      ▼         ▼
 CARD ENGINE   SHOW ENGINE
      │         │
      PNG       MP4
      │         │
      ▼         ▼
  PRODIGI    roast.pet/r/:id
      │
      ▼
  CUSTOMER
```

**`roast.json` is canonical.** Comedy generation decoupled from renderers (Runway/Higgsfield/ElevenLabs are replaceable):

```json
{
  "headline": "JAMES HAS NEVER WON AN ARGUMENT WITH A DOG.",
  "opening": "...",
  "bits": [
    {
      "setup": "...",
      "punchline": "...",
      "reaction": "big_bark"
    }
  ],
  "callback": "...",
  "signoff": "...",
  "card_line": "...",
  "visual": {
    "pet": "biscuit",
    "stage": "roast_v1"
  }
}
```

---

## What V1 does NOT build

No account system. No live Gemini. No pet chat. No persistent Pog memory. No T-shirts. No WebAR image tracking. No multiple show formats. No social network. No mobile app. No automated model router. No elaborate Etsy API integration initially. No autonomous fulfilment until manual fulfilment hurts.

**One pet. One podium. One card. One roast. One scan.**

---

## Development sequence (48-hour build)

1. Create roast.pet visual identity — wordmark, stage, podium, dog audience.
2. Create Biscuit test character from a good source dog photo.
3. Write one genuinely excellent James roast (model-assisted).
4. Produce one 30–45s canonical roast episode.
5. Generate the matching 5×7 Prodigi card artwork at 300dpi.
6. Build `roast.pet/r/biscuit`, mobile-first: video + reroll button.
7. Generate QR, place inside card.
8. Order one real Prodigi sample.
9. Produce Etsy hero thumbnail + 7 secondary images.
10. Cut two silent 15-second Etsy videos.
11. Create Etsy listing with the four personalization inputs.
12. Publish.
13. Fulfil first orders manually.
14. Record every generation, reroll reason, selected take, refund, review.
15. Only automate the steps actual orders prove are bottlenecks.

Distribution note: eligible US listings can now surface through AI shopping (ChatGPT, Gemini/Google AI Mode, Copilot), and stable listing URLs improve off-Etsy discovery. The atomic product must read cold: **PERSONALIZED PET ROAST CARD → SCAN IT → YOUR PET ROASTS YOU.**
