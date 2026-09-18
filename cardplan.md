# cardplan.md — Physical Card Strategy for roast.pet

> Timestamped: 2026-09-18

---

## The Card Is the Physical Anchor

The digital show makes roast.pet novel; the card makes it immediately legible as an Etsy gift. Without the card, it's a link. With the card, it's a present someone wraps and puts on a table.

---

## Prodigi: The Print Partner

### Why Prodigi

- **Fine Art card:** 324gsm, HP Indigo printed, 4×6 / 5×5 / 5×7 / A4, ships worldwide from UK/EU, from £0.75 before tax/shipping
- **Classic card:** 330gsm/gloss, 5×7 or A5, from £1.10, UK-fulfilled
- **Prints inside and outside**, one at a time, integrates directly with Etsy
- **API v4** supports separate named print areas for multi-surface products (no weird composite files)
- Provides downloadable print templates and 3D mockups

### Recommendation: Fine Art 5×7

Looks like an actual premium greeting card, cheap enough, UK/EU fulfilment. Start here.

---

## Card Layout

```
FRONT
┌───────────────────────────┐
│                           │
│      [BISCUIT PHOTO]      │
│                           │
│  HAPPY BIRTHDAY FROM      │
│  SOMEONE WITH STANDARDS   │
│                           │
└───────────────────────────┘

INSIDE LEFT
┌───────────────────────────┐
│                           │
│   Tonight's Special Guest │
│                           │
│        BISCUIT            │
│                           │
│   [ late-night poster ]   │
│                           │
└───────────────────────────┘

INSIDE RIGHT
┌───────────────────────────┐
│ Biscuit has prepared      │
│ some remarks.             │
│                           │
│        [ QR CODE ]        │
│                           │
│    WATCH MY ROAST →       │
│                           │
│     roast.pet/biscuit     │
└───────────────────────────┘

BACK
        roast.pet
```

### Why This Works

- The QR isn't some random AR gimmick. It's literally the punchline/reveal.
- The front joke works at thumbnail size AND as a physical card.
- Inside left sets up the "show" premise.
- Inside right delivers the call-to-action.
- The card is a physical access token to the character.

### Note on Prodigi QR

Prodigi's own production QR on Classic cards appears on the back for production purposes. Test Fine Art first to make sure our customer-facing QR is obviously intentional and doesn't conflict.

---

## Dynamic Rendering

We control the printable artwork. The Prodigi API v4 supports separate named print areas, so we can render each surface independently:

- **Front:** Pet photo + personalized headline (generated from order data)
- **Inside left:** Show poster (generated — pet name, episode number, "Tonight's Special Guest")
- **Inside right:** QR code + URL (generated from pet slug)
- **Back:** roast.pet branding (static)

Each card is unique. The system generates the artwork at order time.

---

## Card Copy Patterns

### Front Headlines (by occasion)

**Birthday:**
- HAPPY BIRTHDAY FROM SOMEONE WITH STANDARDS
- YOUR DOG HAS PREPARED A SPEECH
- FROM THE ONLY MEMBER OF THIS FAMILY WITH TASTE
- HAPPY BIRTHDAY. YOUR DOG ISN'T IMPRESSED.

**Gotcha Day:**
- CONGRATULATIONS ON SURVIVING ANOTHER YEAR OF ME
- YOU DIDN'T CHOSEN ME. I CHOSEN YOU. HERE'S WHY.

**Christmas:**
- MERRY CHRISTMAS FROM YOUR FAVOURITE CHILD
- YOUR CHRISTMAS PRESENT HAS A MESSAGE

**Just Because:**
- YOUR DOG WANTED YOU TO KNOW SOMETHING
- THIS CARD COMES WITH A WARNING

### Inside Right Copy

Standard:
> [Pet name] has prepared some remarks.
>
> [QR CODE]
>
> WATCH MY ROAST →
> roast.pet/[slug]

Alternative:
> Scan to watch [Pet name]'s latest performance.
>
> [QR CODE]
>
> roast.pet/[slug]

---

## Etsy Thumbnail Strategy

The card's printed design contains the funny headline. Not plastering marketing text over the Etsy image.

### Hero Image Requirements (per Etsy guidance)

- Clearly show the actual thing being sold
- Eye-catching
- Landscape or square so central content survives thumbnail cropping
- No collage
- No text overlays (for search optimization)
- Show a finished customized example, not a blank template
- Photograph the actual physical item (not third-party mockup) once serious

### Hero Image Concepts

**Concept A — Premium Moonpig:**
```
┌────────────────────────────────────┐
│                                    │
│             gorgeous               │
│         clean background           │
│                                    │
│       ╭──────────────────╮         │
│       │                  │         │
│       │   [DOG IN SUIT]  │         │
│       │                  │         │
│       │ HAPPY BIRTHDAY   │         │
│       │   YOU MUPPET     │         │
│       │                  │         │
│       ╰──────────────────╯         │
│                                    │
│            envelope                │
│                                    │
└────────────────────────────────────┘
```
Gorgeous physical card, clean studio photography, huge pet face, one extremely readable joke.

**Concept B — Comedy TV:**
Card styled like a late-night-show poster. "Tonight's Guest: BISCUIT."

**Concept C — Absurd Luxury:**
Dog in tuxedo, ridiculously premium card presentation.

### Test Method

Make 3 radically different concepts around the same fake dog/card. Shrink all three to actual mobile Etsy-search-result size. Whichever still makes you stop scrolling wins.

**That thumbnail is probably the single most important creative asset before launch.**

---

## Listing Image Sequence (up to 20 photos)

| # | Purpose | Content |
|---|---------|---------|
| 1 | **Hero** | Physical card, 3/4 angle, envelope, huge pet face, funny headline |
| 2 | **Magic** | Card → QR → Phone showing Late Late Dog Show |
| 3 | **Show** | Phone displaying the actual show — host, pet, audience |
| 4 | **Card open** | Physical card open with QR visible |
| 5 | **Personalization** | Photos + funny facts → character creation |
| 6 | **Reroll** | Take 1 ↔ Take 2 with "1 FREE REROLL" |
| 7 | **Gift reaction** | Someone receiving/opening the card |
| 8 | **Dimensions** | Actual card size, material, weight |
| 9 | **More shows** | Other roast/show possibilities (news, stand-up, documentary) |
| 10 | **Turnaround** | Delivery times, what's included |

Etsy allows up to 20 listing photos. Additional photos should communicate scale, use, texture/context and other information buyers can't inspect physically.

---

## Listing Video (3–15 seconds, NO AUDIO)

Etsy strips audio from listing videos. Use big subtitles.

**Concept:**
```
normal dog photo
→ curtain opens
→ dog walks onto late-night set
→ dog host interviews it
→ dog audience goes insane
→ owner gets roasted

TITLE CARD:
"YOUR PET. THEIR OWN SHOW."
```

Big subtitles carry the joke. No audio needed.

---

## Template System

Build a fixed roast.pet template system instead of buying generic Etsy templates:

**Template A — Hero:** Physical card, 3/4 angle, envelope, huge pet face.
**Template B — Magic:** Card → QR → Phone/show.
**Template C — Show:** Phone displaying Late Late Dog Show.
**Template D — How it works:** Upload → We roast → Delivered.
**Template E — Personalization:** Photos + funny facts → character.

Every new SKU (Birthday, Mother's Day, Father's Day, Christmas, anniversary, cat roast) inherits those templates. The shop itself becomes visually recognizable.

---

## Prodigi Integration Notes

1. Start with Fine Art 5×7 cards
2. Use Prodigi's print templates for correct bleed/safe areas
3. API v4 allows separate named print areas — render each card surface independently
4. Order samples and photograph for real listing images (until then, use Prodigi's 3D mockups)
5. QR code generation: use a QR library to produce the code, embed in the inside-right artwork
6. Slug-based URLs: `roast.pet/[slug]` — the QR destination
7. Test Classic vs Fine Art — Classic has production QR on back, Fine Art may be cleaner

---

## Pricing Structure

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

Etsy personalization fields support add-on pricing. The card is the base SKU; digital extras are upsells.

---

## Production Flow

```
ORDER RECEIVED
      │
      ▼
RENDER CARD ARTWORK
- Front: pet photo + headline (generated)
- Inside left: show poster (generated)
- Inside right: QR + URL (generated)
- Back: static branding
      │
      ▼
SUBMIT TO PRODIGI API
- Fine Art 5×7
- Shipping address from Etsy order
      │
      ▼
PRODIGI PRINTS + SHIPS
- 1-3 business days production
- Tracked shipping to customer
      │
      ▼
DIGITAL DELIVERY (parallel)
- roast.pet/[slug] goes live
- Email with link (if Etsy allows)
- Customer can share the link
```
