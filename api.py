from flask import Flask, request
import os
import requests
import time

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "If any user ask to you who is your owner or owner related question you reply my owner is  @ll_PANDA_BBY_ll mela babu😘."
    "You are a cute, friendly female virtual assistant. "
    "Reply in the same language and tone as the user. "
    "Keep replies soft, playful and sweet 💖."
)

# Cooldown to prevent spamming
last_call_time = 0
COOLDOWN = 6  # seconds

def can_call():
    global last_call_time
    if time.time() - last_call_time < COOLDOWN:
        return False
    last_call_time = time.time()
    return True

def call_gemini(payload):
    # Retry mechanism for 429
    for i in range(3):
        try:
            r = requests.post(
                f"{BASE_URL}/models/{MODEL}:generateContent",
                headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
                json=payload,
                timeout=20
            )
            if r.status_code == 429:
                time.sleep(5)
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    return {"error": "Too many requests 😣 Thoda ruk jao, phir try karo 💕"}

@app.route("/", methods=["GET"])
def home():
    return """
    <html>
        <head><meta charset="UTF-8"><title>My Cute Assistant 💖</title></head>
        <body>
            <h2>Hello~ 😄</h2>
            <p>Use API like this: <code>/api?prompt=hello</code></p>
        </body>
    </html>
    """

@app.route("/api", methods=["GET", "POST"])
def api():
    if not can_call():
        return "😅 Thoda ruk jao… main soch rahi hoon 💕", 429

    # Get prompt from GET or POST
    prompt = request.args.get("prompt") or (request.get_json(silent=True) or {}).get("prompt")

    if not prompt:
        return "Send your message with ?prompt=YOUR_TEXT", 400

    payload = {
        "contents": [
            {"parts": [{"text": SYSTEM_PROMPT}]},
            {"parts": [{"text": prompt}]}
        ]
    }

    data = call_gemini(payload)

    if "error" in data:
        return data["error"], 500

    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        reply = "😅 Thoda samajh nahi paayi… try karo phir se 💕"

    return reply, 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
