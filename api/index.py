import json
import os
import requests
from urllib.parse import parse_qs

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-2.5-flash"

# Cute female assistant style
SYSTEM_PROMPT = (
    "You are a cute, friendly female virtual assistant. "
    "Reply in the same language and tone as the user. "
    "Keep replies sweet, soft, and playful 💖."
)

def handler(request):
    # GET parameter support
    query = parse_qs(request.query_string.decode())
    prompt = query.get("prompt", [None])[0]

    # fallback to POST body
    if not prompt:
        try:
            body = json.loads(request.body or "{}")
            prompt = body.get("prompt")
        except:
            prompt = None

    if not prompt:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": "Hello~ tum message bhejo `?prompt=YOUR_TEXT` ke saath 😄"
        }

    # Call Gemini API
    try:
        url = f"{BASE_URL}/models/{MODEL}:generateContent"
        headers = {
            "x-goog-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {"parts": [{"text": SYSTEM_PROMPT}]},
                {"parts": [{"text": prompt}]}
            ]
        }

        r = requests.post(url, headers=headers, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        # Return plain text for browser
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": reply
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": f"Error: {e}"
        }
