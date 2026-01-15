from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AI API is running"

@app.route("/ask", methods=["GET", "POST"])
def ask():
    msg = request.args.get("message") or request.json.get("message")
    if not msg:
        return jsonify({"error": "No message provided"}), 400

    # Dummy AI reply (test)
    reply = f"You asked: {msg}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
