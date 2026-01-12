from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_roadmap(year, interest, branch):
    """
    Generate a roadmap based on student's year, interest, and branch.
    
    Args:
        year (str): Student's current year (e.g., "1", "2", "3", "4")
        interest (str): Area of interest (e.g., "Web Development", "Data Science")
        branch (str): Engineering branch (e.g., "CSE", "IT", "ECE")
    
    Returns:
        dict: Roadmap containing difficulty level and steps
    """
    # Determine difficulty level based on year
    difficulty_map = {
        "1": "Beginner",
        "2": "Intermediate",
        "3": "Advanced",
        "4": "Expert"
    }
    difficulty_level = difficulty_map.get(year, "Intermediate")
    
    # Generate sample roadmap steps based on interest
    roadmap_templates = {
        "Web Development": [
            "Learn HTML, CSS, and JavaScript fundamentals",
            "Master a frontend framework (React, Vue, or Angular)",
            "Learn backend development with Node.js or Python",
            "Understand databases (SQL and NoSQL)",
            "Build full-stack projects and deploy them",
            "Learn about API design and RESTful services"
        ],
        "Data Science": [
            "Learn Python programming and data structures",
            "Master pandas, NumPy, and data manipulation",
            "Study statistics and probability",
            "Learn machine learning algorithms",
            "Work with data visualization tools",
            "Build end-to-end ML projects"
        ],
        "Mobile Development": [
            "Learn mobile app fundamentals",
            "Choose a platform (iOS/Android) or go cross-platform",
            "Master UI/UX design principles",
            "Learn state management and navigation",
            "Integrate APIs and backend services",
            "Publish apps to app stores"
        ]
    }
    
    # Get steps based on interest or provide default
    steps = roadmap_templates.get(
        interest,
        [
            "Identify core fundamentals in your field",
            "Build foundational knowledge through courses",
            "Work on practical projects",
            "Contribute to open source",
            "Network with professionals",
            "Keep learning and stay updated"
        ]
    )
    
    return {
        "difficulty_level": difficulty_level,
        "steps": steps
    }

@app.route('/api/roadmap', methods=['POST'])
def create_roadmap():
    """
    Endpoint to generate a personalized roadmap.
    
    Expected JSON input:
    {
        "name": "Student Name",
        "year": "1-4",
        "branch": "Engineering Branch",
        "interest": "Area of Interest"
    }
    
    Returns:
    {
        "name": "Student Name",
        "year": "1-4",
        "branch": "Engineering Branch",
        "interest": "Area of Interest",
        "difficulty_level": "Beginner/Intermediate/Advanced/Expert",
        "steps": ["step1", "step2", ...]
    }
    """
    try:
        # Parse request data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'year', 'branch', 'interest']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract input data
        name = data['name']
        year = data['year']
        branch = data['branch']
        interest = data['interest']
        
        # Generate roadmap
        roadmap_data = get_roadmap(year, interest, branch)
        
        # Prepare response
        response = {
            'name': name,
            'year': year,
            'branch': branch,
            'interest': interest,
            'difficulty_level': roadmap_data['difficulty_level'],
            'steps': roadmap_data['steps']
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)