# etsysignal

Etsy intelligence + voice commerce. What to sell, how to sell it, and the tools to do it.

## What We're Building

1. **Game Winner** — Personalized sports video gifts (zero competition on Etsy)
2. **Voice Commerce** — Speaking/ramble flow for Google + ChatGPT live models
3. **Etsy Data** — Sales estimates calibrated against real data

## Quick Start

```bash
python3 tools/etsy_snapshot.py          # Capture current metrics
python3 strats/game_winner.py          # Game Winner strategy
python3 voice/ramble_flow.py           # Voice commerce demo
```

## Structure

```
strats/        — What to sell and why
data/          — Analysis and research
tools/         - Etsy API, snapshots, scraping
voice/         — Voice commerce (Google/ChatGPT live models)
```
