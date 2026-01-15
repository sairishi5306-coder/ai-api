from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# API KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ROOT (TEST)
@app.route("/", methods=["GET"])
def root():
    return "SERVER OK - AI READY"

# AI ROUTE
@app.route("/ask", methods=["GET"])
def ask_ai():
    q = request.args.get("me")

    if not q:
        return jsonify({"error": "Use ?me=your_question"})

    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        r = model.generate_content(q)

        return jsonify({
            "question": q,
            "answer": r.text
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
