from flask import Flask, request, jsonify
import os
from typing import List, Dict

APP_NAME = "ACEest Fitness & Gym"
VERSION = "1.2.3"

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

@app.get("/workouts")
def get_workouts():
    return jsonify({"count": len(workouts), "items": workouts}), 200

@app.post("/workouts")
def add_workout():
    data = request.get_json(silent=True) or {}
    kind = data.get("type")
    minutes = data.get("minutes")

    # Basic validation
    if not isinstance(kind, str) or not kind.strip():
        return jsonify({"error": "type is required"}), 400
    try:
        minutes = int(minutes)
    except Exception:
        return jsonify({"error": "minutes must be an integer"}), 400
    if minutes <= 0:
        return jsonify({"error": "minutes must be > 0"}), 400

    workouts.append({"type": kind.strip(), "minutes": minutes})
    return jsonify({"ok": True, "added": {"type": kind, "minutes": minutes}}), 201

@app.get("/stats")
def stats():
    total = sum(w.get("minutes", 0) for w in workouts)
    by_type = {}
    for w in workouts:
        by_type[w["type"]] = by_type.get(w["type"], 0) + w["minutes"]
    return jsonify({"count": len(workouts), "total_minutes": total, "by_type": by_type}), 200

@app.get("/summary")
def summary():
    total = sum(w.get("minutes", 0) for w in workouts)
    return jsonify({"summary": f"Workouts: {len(workouts)} | Total minutes: {total} | Version: {VERSION}"}), 200

if __name__ == "__main__":
    # Bind to 0.0.0.0 for container use
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
