from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("me")
    if not question:
        return jsonify({"error": "question missing"}), 400

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)
    data = response.json()

    try:
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"answer": answer})
    except:
        return jsonify({"error": "AI response invalid", "raw": data})

if __name__ == "__main__":
    app.run()
