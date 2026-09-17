# Gemini Live API — Quick Reference

## Overview
- Low-latency, real-time voice + vision
- 97 languages, barge-in, tool use
- Audio: 16kHz input, 24kHz output
- Protocol: WebSocket (WSS)

## Pricing
- Input: $0.005/min
- Output: $0.018/min
- 1,000 conversations × 2min = $10/month

## Key Features
- Multilingual (97 languages)
- Barge-in (interrupt model)
- Tool use (function calling)
- Audio transcriptions
- Proactive audio
- Affective dialog

## Get Started

### Python (GenAI SDK)
```python
from google import genai

client = genai.Client()
session = client.aio.live.connect(model="gemini-3.8-live")

# Send audio
await session.send_realtime_input(audio=audio_data)

# Receive response
response = await session.receive()
```

### JavaScript (WebSocket)
```javascript
const ws = new WebSocket("wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent");

// Send setup
ws.send(JSON.stringify({
  setup: {
    model: "models/gemini-3.8-live",
    generationConfig: { responseModalities: ["AUDIO"] }
  }
}));
```

## Partners
- LiveKit
- Pipecat (Daily)
- Fishjam
- Vision Agents
- Agora
- Firebase AI SDK

## Use Cases
- E-commerce shopping assistants
- Gaming NPCs
- Healthcare companions
- Financial advisors
- Education mentors
- Live translation
