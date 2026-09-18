# roast.pet — Checkpoint 1 Demo Pack

This is a synthetic Etsy customer fixture for the first end-to-end product checkpoint.

## Checkpoint 1

Given only the contents of `02_customer_uploads/buster-001/`, the system must produce:

1. a normalized persistent Pog identity,
2. a usable animated avatar with mouth/lip movement,
3. a 30–60 second birthday roast performance,
4. a print-ready personalized birthday card,
5. a unique QR/reveal URL,
6. a mobile AR/reveal experience in which the same pet appears to come alive from the card.

Comedy quality is deliberately **not** the primary pass/fail criterion yet. Identity fidelity, deterministic flow,
asset provenance, reliable rendering, card production, and AR handoff are.

The pack intentionally contains both good and bad customer photos so the intake validator has something real to reject.

## Folder map

- `00_research_notes/` — current Etsy personalization constraints and product model
- `01_etsy_listing_fixture/` — the exact five-question listing configuration
- `02_customer_uploads/` — fake Etsy order as the backend should receive it
- `03_expected_normalization/` — target structured data after intake/cleaning
- `04_pipeline_contracts/` — machine-readable contracts for each processing stage
- `05_card/` — target physical card contract and copy fixture
- `06_ar/` — AR target / QR / reveal contracts
- `07_video/` — performance timing and mouth-motion contracts
- `08_qa/` — checkpoint acceptance tests and failure cases
- `09_edge_cases/` — alternate orders that should fail or degrade gracefully

## Canonical command target

Eventually one command should take the raw order to all outputs:

```bash
python -m roastpet.checkpoint1 02_customer_uploads/buster-001/order_raw_etsy.json
```

Expected final manifest:

```text
PASS intake
PASS photo_qc
PASS pog_identity
PASS avatar
PASS lipsync
PASS card
PASS qr
PASS reveal
PASS ar
PASS video
```
