import json
import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "You are a cute, friendly female virtual assistant. "
    "Reply in the same language and tone as the user. "
    "Keep replies sweet, soft, and playful."
)

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Only POST allowed"})
        }

    body = json.loads(request.body or "{}")
    prompt = body.get("prompt")

    if not prompt:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "prompt required"})
        }

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
    data = r.json()

    reply = data["candidates"][0]["content"]["parts"][0]["text"]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"reply": reply})
    }
