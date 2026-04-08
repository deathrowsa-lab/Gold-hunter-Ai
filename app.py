from flask import Flask
import os

# Initialize the Flask application
app = Flask(__name__)

@app.route("/")
def home():
    return "Gold Hunter AI is running 🚀"

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
