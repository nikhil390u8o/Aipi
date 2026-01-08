from flask import Flask, request
import os
import requests
from urllib.parse import unquote

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "If any user ask about your owner you will reply with cute message my owner is @ll_PANDA_BBY_ll mera babu😘."
    "You are a cute, friendly female virtual assistant. "
    "Reply in the same language and tone as the user. "
    "Keep replies soft, playful and sweet 💖."
)

@app.route("/", methods=["GET"])
def home():
    return """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>My Cute Assistant 💖</title>
        </head>
        <body>
            <h2>Hello~ 😄</h2>
            <p>Use API like this: <code>/api?prompt=hello</code></p>
        </body>
    </html>
    """

@app.route("/api", methods=["GET", "POST"])
def api():
    # GET parameter
    prompt = request.args.get("prompt")

    # fallback POST
    if not prompt:
        try:
            data = request.get_json(silent=True) or {}
            prompt = data.get("prompt")
        except:
            prompt = None

    if not prompt:
        return "Send your message with ?prompt=YOUR_TEXT", 400

    try:
        # Call Gemini API
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

        return reply, 200, {"Content-Type": "text/plain; charset=utf-8"}

    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
