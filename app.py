from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AI API is running"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "Question empty"}), 400

    # Simple demo AI reply
    answer = f"You asked: {question}"

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
