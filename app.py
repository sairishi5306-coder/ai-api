from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# ✅ Gemini API key (Render Environment Variable से)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    return_text = "GEMINI_API_KEY environment variable set नहीं है"
    raise RuntimeError(return_text)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# 🔹 Root route (SLASH) – इसे change नहीं किया
@app.route("/", methods=["GET"])
def home():
    return "AI API is running"

# 🔹 AI वाला route
@app.route("/ask", methods=["GET", "POST"])
def ask():
    msg = request.args.get("message")

    if request.is_json:
        msg = request.json.get("message")

    if not msg:
        return jsonify({"error": "Message नहीं मिला"}), 400

    try:
        response = model.generate_content(msg)
        return jsonify({
            "reply": response.text
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
