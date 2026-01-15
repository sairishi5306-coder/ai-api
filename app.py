from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "SERVER OK - AI READY"

@app.route("/ask")
def ask():
    q = request.args.get("me")
    if not q:
        return jsonify({"error": "use ?me=question"})

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    r = model.generate_content(q)

    return jsonify({"answer": r.text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
