from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Gold Hunter AI Running 🚀"

@app.route("/status")
def status():
    return jsonify({
        "bot": "running",
        "trades_today": 0,
        "profit": 0
    })

app.run(host="0.0.0.0", port=10000)
