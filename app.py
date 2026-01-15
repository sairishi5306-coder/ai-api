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

    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        "gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": msg}
                ]
            }
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=30)
        data = r.json()

        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": "AI request failed", "details": str(e)}), 500


if __name__ == "__main__":
    app.run()
