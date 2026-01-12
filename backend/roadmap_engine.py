import json
import os

# Load roadmap data once
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "roadmaps.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    ROADMAP_DATA = json.load(f)

# Difficulty multiplier by year
YEAR_DIFFICULTY = {
    "1st Year": 1,
    "2nd Year": 2,
    "3rd Year": 3,
    "4th Year": 4
}

def get_difficulty_label(year):
    level = YEAR_DIFFICULTY.get(year, 1)
    if level == 1:
        return "Foundation"
    if level == 2:
        return "Intermediate"
    if level == 3:
        return "Advanced"
    return "Industry Ready"


def get_roadmap(year, interest, branch):
    """
    Core brain of the system.
    - Decides roadmap by year
    - Scales difficulty automatically
    - Branch can fine-tune focus
    """

    difficulty_level = get_difficulty_label(year)

    # Get interest-specific roadmap
    interest_data = ROADMAP_DATA.get(interest, {})
    year_steps = interest_data.get(year, [])

    enriched_steps = []

    for step in year_steps:
        enriched_steps.append({
            "step": step.get("step"),
            "title": step.get("title"),
            "description": step.get("description"),
            "skills": step.get("skills"),
            "tools": step.get("tools"),
            "outcome": step.get("outcome"),
            "difficulty": difficulty_level,
            "branch_focus": branch
        })

    return {
        "year": year,
        "interest": interest,
        "branch": branch,
        "difficulty_level": difficulty_level,
        "steps": enriched_steps
    }
