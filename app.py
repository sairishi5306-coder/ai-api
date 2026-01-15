@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        message = request.args.get("message")
        key = request.args.get("key")
    else:
        data = request.get_json(silent=True) or {}
        message = data.get("message")
        key = data.get("key")

    if key != "SGXCODEX":
        return jsonify({"error": "Invalid API Key"}), 401

    if not message:
        return jsonify({"error": "Message missing"}), 400

    headers = {
        "Authorization": f"Bearer {SAMBA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "ALLaM-7B-Instruct-preview",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": message}
        ]
    }

    r = requests.post(SAMBA_URL, headers=headers, json=payload, timeout=30)
    data = r.json()

    reply = data["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})
