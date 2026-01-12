from flask import Flask, request, jsonify
from flask_cors import CORS
from roadmap_engine import get_roadmap

app = Flask(__name__)
CORS(app)

@app.route("/api/roadmap", methods=["GET", "POST"])
def roadmap():
    if request.method == "POST":
        data = request.get_json()
        interest = data.get("interest")
        year = int(data.get("year"))
        name = data.get("name", "")
        branch = data.get("branch", "")
    else:
        interest = request.args.get("interest")
        year = int(request.args.get("year", 1))
        name = ""
        branch = ""

    roadmap = get_roadmap(interest, year)

    return jsonify({
        "name": name,
        "branch": branch,
        "interest": interest,
        "year": year,
        "roadmap": roadmap
    })

if __name__ == "__main__":
    app.run(debug=True)
