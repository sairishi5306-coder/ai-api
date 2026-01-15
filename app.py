from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Real AI API is running"

@app.route("/ask", methods=["GET", "POST"])
def ask():
    msg = None

    if request.method == "GET":
        msg = request.args.get("message")
    else:
        data = request.get_json(silent=True)
        if data:
            msg = data.get("message")

    if not msg:
        return jsonify({"error": "No message provided"}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API key missing"}), 500

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": msg}
                ]
            }
        ]
    }

    r = requests.post(url, json=payload, timeout=30)

    if r.status_code != 200:
        return jsonify({"error": "AI request failed", "details": r.text}), 500

    data = r.json()

    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "AI जवाब नहीं दे पाया"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
