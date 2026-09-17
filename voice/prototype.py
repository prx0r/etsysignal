"""Voice Commerce Prototype — Gemini Live + Etsy API.

Flow: Voice → Intent → Search → Preview → Purchase → Delivery
"""
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# Etsy API
ETSY_KEY = os.environ.get("ETSY_API_KEY", "")
ETSY_SECRET = os.environ.get("ETSY_SHARED_SECRET", "")

def etsy_search(keywords, limit=5):
    """Search Etsy listings."""
    url = f"https://openapi.etsy.com/v3/application/listings/active?keywords={quote(keywords)}&limit={limit}"
    req = Request(url, headers={"x-api-key": f"{ETSY_KEY}:{ETSY_SECRET}"})
    try:
        with urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            return data.get("results", [])
    except:
        return []


def handle_voice_intent(intent, slots):
    """Process voice intent and return response."""
    
    if intent == "search_product":
        # Customer wants to find a product
        keywords = slots.get("product", "personalized gift")
        listings = etsy_search(keywords, 3)
        
        if not listings:
            return {"text": "I couldn't find any results for that. Try being more specific."}
        
        response = f"I found {len(listings)} options for {keywords}:\n"
        for i, l in enumerate(listings[:3], 1):
            price = l.get("price", {}).get("amount", 0) / l.get("price", {}).get("divisor", 1)
            response += f"{i}. {l.get('title', '?')[:50]} - ${price:.2f}\n"
        response += "\nWhich one would you like?"
        return {"text": response, "listings": listings}
    
    elif intent == "buy_product":
        # Customer wants to buy
        listing_id = slots.get("listing_id")
        return {"text": f"Great choice! Processing your order for listing {listing_id}. Your personalized video will be ready in 24 hours."}
    
    elif intent == "customize":
        # Customer wants to customize
        return {"text": "I'd love to help personalize your video! What's the recipient's name and what team do they support?"}
    
    return {"text": "I can help you find personalized gifts. What are you looking for?"}


# Gemini Live API integration
def create_voice_agent():
    """Create a Gemini Live voice agent."""
    # This would connect to Gemini Live API
    # For now, return the agent config
    return {
        "model": "gemini-3.8-live",
        "tools": [
            {"name": "search_product", "description": "Search Etsy for products"},
            {"name": "buy_product", "description": "Purchase a product"},
            {"name": "customize", "description": "Customize a product"},
        ],
        "voice": "Aoede",
        "language": "en",
    }


if __name__ == "__main__":
    # Test the voice agent
    agent = create_voice_agent()
    print(json.dumps(agent, indent=2))
    
    # Test intent handling
    print("\nTest search:")
    result = handle_voice_intent("search_product", {"product": "personalized football video gift"})
    print(result["text"])
