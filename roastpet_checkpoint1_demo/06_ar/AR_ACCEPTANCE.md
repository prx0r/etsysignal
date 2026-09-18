# AR / reveal acceptance

V1 checkpoint can have two modes:

## Guaranteed reveal
QR opens the private mobile reveal page and plays the same Pog performance.

## AR enhancement
After permission, camera recognizes the printed card front (or uses the QR as explicit anchor)
and renders the Pog aligned to the card.

PASS:
- scan works from an ordinary printed card
- same Pog identity as video
- stable enough tracking for a 10+ second performance
- audio starts only after user interaction where mobile browser policy requires it
- fallback reveal works when camera/AR is unsupported

FAIL:
- AR is the only way to access the gift
- different-looking pet in AR vs video
- card target requires hidden production metadata
