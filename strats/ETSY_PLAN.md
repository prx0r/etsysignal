# Etsy Canonical Plan — Pet Roast Birthday Gift

## Strategy

**Brand tone:** UK-first
**Sales market:** UK + US from day one
**Don't build separate stores** — suppliers handle logistics

---

## The Product

**Personalised Pet Birthday Roast Card + Video**

Upload your pet → enter birthday gossip → receive printed card → scan QR → dog performs roast.

---

## Etsy Listing (5 Questions)

| # | Type | Question | What it feeds |
|---|------|----------|---------------|
| 1 | File upload | Upload your pet photos | Pog visual identity |
| 2 | Text | Who are we roasting? | name, age, relationship |
| 3 | Text | Give us the gossip | jokes/stories |
| 4 | Dropdown | How savage? (Sweet/Cheeky/Savage/Unhinged) | roast tone |
| 5 | Text | Birthday sign-off | affectionate closer |

---

## Three Launch SKUs

### 1. Birthday Roast Card (Hero)
- Physical card + digital roast video
- QR inside card → pog.pet
- Price: £2.99 + £1.49 shipping

### 2. Savage Birthday Roast
- Same engine, comedy-focused positioning
- For mates, siblings, 30th/40th/50th

### 3. From the Dog Birthday Card
- Softer, "card from the dog" angle
- Same runtime, different positioning

---

## Card Layout (Prodigi 7x5")

**Front:**
> JAMES IS 50.
> BUSTER HAS NOTES.
> A birthday roast from the dog who knows too much.

**Inside Left:**
> "James says I sleep all day.
> James owns golf clubs and still shoots 110.
> We all have hobbies."
> [Pog.pet branding]

**Inside Right:**
> Happy 50th Dad. Love Sophie and Buster.
> [Large QR code]
> BUSTER'S NOT FINISHED.
> Scan to watch his birthday roast ↓
> pog.pet/r/7FJ3K2

**Back:**
> Made alive by Pog.pet

---

## Prodigi Details

- Classic greeting card: from £1.10
- Production: 24 hours (UK)
- Ships: worldwide
- 330gsm Fedrigoni stock
- 5×7" or A5
- Customisable inside and out
- Envelope included
- Etsy integration

---

## Pricing

| Product | Cost | Price | Margin |
|---------|------|-------|--------|
| Card | £1.10 | £2.99 | 63% |
| Card + shipping | £1.10 + £1.49 | £4.48 | 75% |
| Mug | £3.65 | £4.49 | 19% |
| Mug + shipping | £3.65 + £1.99 | £6.48 | 43% |
| Card + Mug bundle | £4.75 | £6.99 | 32% |

---

## Architecture

```
ETSY LISTING
    │
    ├── pet photos (upload)
    ├── recipient (text)
    ├── gossip (text)
    ├── savage level (dropdown)
    └── sign-off (text)
    │
    ▼
RoastOrder
    │
    ▼
FREAKTOWN
script → beats → TTS → avatar → performance
    │
    ├──────────────┐
    ▼              ▼
PRINT ART       POG PERFORMANCE
    │              │
    ▼              ▼
PRODIGI          pog.pet/r/...
    │              ▲
    ▼              │
PHYSICAL CARD ── QR
                   │
                   ▼
              persistent Pog
```

---

## ChatGPT Integration (Phase 2)

Etsy now supports ChatGPT, Gemini, Google AI Mode, Copilot.

User: "I forgot my dad's birthday. He loves his dachshund."
ChatGPT: Surfaces our listing.

Later: ChatGPT calls pog.pet functions directly.
