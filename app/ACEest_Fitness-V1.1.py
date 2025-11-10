from flask import Flask, request, jsonify
import os
from typing import List, Dict

APP_NAME = "ACEest Fitness & Gym"
VERSION = "1.1"

app = Flask(__name__)

# in-memory store (demo purposes)
workouts: List[Dict] = []

@app.get("/")
def home():
    return jsonify({"app": APP_NAME, "version": VERSION}), 200

@app.get("/health")
def health():
    return "OK", 200

@app.get("/bmi")
def bmi():
    """Compute BMI given height_cm and weight_kg as query params."""
    try:
        h = float(request.args.get("height_cm", ""))
        w = float(request.args.get("weight_kg", ""))
    except ValueError:
        return jsonify({"error": "height_cm and weight_kg must be numbers"}), 400
    if h <= 0 or w <= 0:
        return jsonify({"error": "height_cm and weight_kg must be > 0"}), 400
    m = h / 100.0
    bmi_val = round(w / (m * m), 2)
    return jsonify({"bmi": bmi_val, "height_cm": h, "weight_kg": w}), 200

if __name__ == "__main__":
    # Bind to 0.0.0.0 for container use
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)

