import json
import os
import requests
from urllib.parse import parse_qs

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "You are a cute, friendly female virtual assistant. "
    "Reply in the same language and tone as the user. "
    "Keep replies sweet, soft, and playful 💖."
)

def handler(request):
    # GET parameter
    query = parse_qs(request.query_string.decode())
    prompt = query.get("prompt", [None])[0]

    # fallback POST
    if not prompt:
        try:
            body = json.loads(request.body or "{}")
            prompt = body.get("prompt")
        except:
            prompt = None

    # No prompt → show message in HTML
    if not prompt:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": "<h2>Hello~ 😄</h2><p>Message bhejo URL me <b>?prompt=YOUR_TEXT</b> ke saath!</p>"
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

        # Return reply as HTML
        html = f"<h2>Assistant 💖</h2><p>{reply}</p>"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": html
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": f"<p>Error: {e}</p>"
        }
