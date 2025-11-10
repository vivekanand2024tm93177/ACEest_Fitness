from flask import Flask, request, jsonify
import os
from typing import List, Dict

APP_NAME = "ACEest Fitness & Gym"
VERSION = "1.0"

app = Flask(__name__)

# in-memory store (demo purposes)
workouts: List[Dict] = []

@app.get("/")
def home():
    return jsonify({"app": APP_NAME, "version": VERSION}), 200

@app.get("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Bind to 0.0.0.0 for container use
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
