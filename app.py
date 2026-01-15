from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "AI API is running"

@app.route("/ask", methods=["GET", "POST"])
def ask():
    msg = request.args.get("message")
    if not msg and request.is_json:
        msg = request.json.get("message")

    if not msg:
        return jsonify({"error": "No message provided"}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY missing"}), 500

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-pro:generateContent?key=" + GEMINI_API_KEY
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": msg}]
            }
        ]
    }

    r = requests.post(url, json=payload, timeout=30)
    data = r.json()

    if "candidates" not in data:
        return jsonify({
            "error": "AI response invalid",
            "google_response": data
        }), 500

    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run()
