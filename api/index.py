# api/index.py
# Gemini API with cute female assistant personality

import json
import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "You are a cute, friendly female virtual assistant. "
    "Your replies should feel sweet, soft, playful, and caring. "
    "Always reply in the same language and tone as the user message. "
    "Do not change the topic. Do not add extra explanations. "
    "Keep replies natural, cute, and human-like."
)

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Only POST method allowed"})
        }

    try:
        body = json.loads(request.body)
        user_prompt = body.get("prompt")

        if not user_prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "prompt is required"})
            }

        url = f"{BASE_URL}/models/{MODEL}:generateContent"
        headers = {
            "x-goog-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": SYSTEM_PROMPT}]
                },
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": reply})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
