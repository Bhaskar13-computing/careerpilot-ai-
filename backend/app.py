from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "CareerPilot AI backend is running"


ROADMAP_FILE = "roadmaps.json"

# ---------------- UTIL ---------------- #

def load_roadmaps():
    with open(ROADMAP_FILE, "r") as f:
        return json.load(f)

# ---------------- API: ROADMAP ---------------- #

@app.route("/get-roadmap", methods=["POST"])
def get_roadmap():
    data = request.json

    branch = data.get("branch")
    year = data.get("year")
    interest = data.get("interest")

    key = f"{branch}_{year}_{interest}"

    roadmaps = load_roadmaps()
    roadmap = roadmaps.get(key, [])

    if not roadmap:
        return jsonify({
            "error": "No roadmap found for selected options"
        }), 404

    return jsonify({
        "roadmap": roadmap
    })

# ---------------- API: CHATBOT ---------------- #

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").lower()

    # simple intelligent responses
    if "start" in message or "begin" in message:
        reply = "Start with the first topic in your roadmap and focus on fundamentals."

    elif "tools" in message:
        reply = "Focus on tools mentioned in the current roadmap step."

    elif "confused" in message or "stuck" in message:
        reply = "Take one topic at a time. Practice daily and revise weekly."

    elif "job" in message or "career" in message:
        reply = "Stay consistent with this roadmap. Skills matter more than certificates."

    else:
        reply = "Follow your roadmap step by step and practice regularly."

    return jsonify({
        "reply": reply
    })

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
