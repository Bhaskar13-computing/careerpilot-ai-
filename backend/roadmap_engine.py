import json
import os
from typing import Dict, List, Optional


class RoadmapEngine:
    """
    Engine for generating personalized career roadmaps based on student profile.
    """
    
    def __init__(self, data_path: str = "data/roadmaps.json"):
        """
        Initialize the roadmap engine with data from JSON file.
        
        Args:
            data_path (str): Path to the roadmaps JSON file
        """
        self.data_path = data_path
        self.roadmaps_data = self._load_roadmaps()
        
        # Difficulty mapping based on year
        self.difficulty_mapping = {
            "1": "Beginner",
            "2": "Intermediate",
            "3": "Advanced",
            "4": "Expert"
        }
    
    def _load_roadmaps(self) -> Dict:
        """
        Load roadmap data from JSON file.
        
        Returns:
            Dict: Loaded roadmap data
        """
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"Warning: {self.data_path} not found. Using default data.")
                return self._get_default_roadmaps()
        except Exception as e:
            print(f"Error loading roadmaps: {e}. Using default data.")
            return self._get_default_roadmaps()
    
    def _get_default_roadmaps(self) -> Dict:
        """
        Provide default roadmap structure if JSON file is not available.
        
        Returns:
            Dict: Default roadmap data
        """
        return {
            "interests": {
                "Web Development": {
                    "description": "Full-stack web development path",
                    "branches": {
                        "CSE": {
                            "1": [
                                "Learn HTML5, CSS3, and JavaScript fundamentals",
                                "Understand DOM manipulation and events",
                                "Build 3-5 static websites",
                                "Learn Git and GitHub basics",
                                "Study responsive design principles"
                            ],
                            "2": [
                                "Master a frontend framework (React/Vue/Angular)",
                                "Learn Node.js and Express.js",
                                "Understand RESTful API design",
                                "Work with SQL databases (PostgreSQL/MySQL)",
                                "Build 2-3 full-stack projects"
                            ],
                            "3": [
                                "Learn advanced React patterns (hooks, context, Redux)",
                                "Master backend frameworks (Django/Flask/Spring)",
                                "Implement authentication and authorization",
                                "Work with NoSQL databases (MongoDB)",
                                "Learn Docker and containerization",
                                "Build scalable microservices"
                            ],
                            "4": [
                                "Master cloud platforms (AWS/Azure/GCP)",
                                "Implement CI/CD pipelines",
                                "Learn system design and architecture",
                                "Study performance optimization",
                                "Contribute to open-source projects",
                                "Build production-ready applications"
                            ]
                        }
                    }
                },
                "Data Science": {
                    "description": "Data science and machine learning path",
                    "branches": {
                        "CSE": {
                            "1": [
                                "Learn Python programming fundamentals",
                                "Master data structures and algorithms",
                                "Study basic statistics and mathematics",
                                "Learn pandas and NumPy basics",
                                "Work on simple data analysis projects"
                            ],
                            "2": [
                                "Master pandas, NumPy, and Matplotlib",
                                "Learn probability and statistical inference",
                                "Study supervised learning algorithms",
                                "Work with scikit-learn library",
                                "Complete 3-4 ML projects on Kaggle"
                            ],
                            "3": [
                                "Learn deep learning with TensorFlow/PyTorch",
                                "Study neural networks and CNNs",
                                "Master data visualization (Seaborn, Plotly)",
                                "Work with big data tools (Spark, Hadoop)",
                                "Build end-to-end ML pipelines",
                                "Learn MLOps fundamentals"
                            ],
                            "4": [
                                "Master advanced ML techniques (NLP, Computer Vision)",
                                "Learn model deployment and monitoring",
                                "Study distributed systems and scalability",
                                "Contribute to research or open-source ML projects",
                                "Build production ML systems",
                                "Prepare portfolio for data science roles"
                            ]
                        }
                    }
                },
                "Mobile Development": {
                    "description": "iOS and Android mobile app development",
                    "branches": {
                        "CSE": {
                            "1": [
                                "Learn Java or Kotlin fundamentals",
                                "Understand OOP concepts thoroughly",
                                "Study mobile UI/UX principles",
                                "Build 2-3 simple Android apps",
                                "Learn Android Studio basics"
                            ],
                            "2": [
                                "Master Android development (Activities, Fragments)",
                                "Learn React Native or Flutter",
                                "Study mobile app architecture patterns (MVVM, MVI)",
                                "Work with REST APIs and JSON",
                                "Build cross-platform mobile apps"
                            ],
                            "3": [
                                "Learn advanced state management (Redux, Bloc)",
                                "Master native features (camera, GPS, sensors)",
                                "Implement push notifications and analytics",
                                "Study app performance optimization",
                                "Build apps with backend integration",
                                "Learn mobile security best practices"
                            ],
                            "4": [
                                "Master app deployment (Play Store, App Store)",
                                "Learn CI/CD for mobile apps",
                                "Study advanced animations and custom UI",
                                "Build production-quality apps",
                                "Contribute to mobile open-source projects",
                                "Create a strong app portfolio"
                            ]
                        }
                    }
                }
            }
        }
    
    def get_difficulty_level(self, year: str) -> str:
        """
        Determine difficulty level based on student's year.
        
        Args:
            year (str): Student's current year (1-4)
        
        Returns:
            str: Difficulty level
        """
        return self.difficulty_mapping.get(year, "Intermediate")
    
    def get_roadmap_steps(self, year: str, interest: str, branch: str) -> List[str]:
        """
        Get roadmap steps based on year, interest, and branch.
        
        Args:
            year (str): Student's current year (1-4)
            interest (str): Area of interest
            branch (str): Engineering branch
        
        Returns:
            List[str]: List of roadmap steps
        """
        try:
            # Navigate through the data structure
            interest_data = self.roadmaps_data.get("interests", {}).get(interest)
            
            if not interest_data:
                return self._get_generic_roadmap(year)
            
            # Try to get branch-specific roadmap
            branch_data = interest_data.get("branches", {}).get(branch)
            
            if not branch_data:
                # If branch not found, use any available branch
                branch_data = next(iter(interest_data.get("branches", {}).values()), None)
            
            if not branch_data:
                return self._get_generic_roadmap(year)
            
            # Get year-specific steps
            steps = branch_data.get(year)
            
            if not steps:
                # If year not found, try to get closest year
                steps = self._get_closest_year_steps(branch_data, year)
            
            return steps if steps else self._get_generic_roadmap(year)
            
        except Exception as e:
            print(f"Error getting roadmap steps: {e}")
            return self._get_generic_roadmap(year)
    
    def _get_closest_year_steps(self, branch_data: Dict, year: str) -> Optional[List[str]]:
        """
        Get steps from the closest available year if exact year not found.
        
        Args:
            branch_data (Dict): Branch-specific data
            year (str): Target year
        
        Returns:
            Optional[List[str]]: Steps from closest year or None
        """
        available_years = sorted(branch_data.keys())
        if not available_years:
            return None
        
        # Find closest year
        year_int = int(year)
        closest_year = min(available_years, key=lambda y: abs(int(y) - year_int))
        
        return branch_data.get(closest_year)
    
    def _get_generic_roadmap(self, year: str) -> List[str]:
        """
        Provide a generic roadmap when specific data is not available.
        
        Args:
            year (str): Student's current year
        
        Returns:
            List[str]: Generic roadmap steps
        """
        generic_steps = {
            "1": [
                "Build strong programming fundamentals",
                "Learn data structures and basic algorithms",
                "Complete online courses in your interest area",
                "Work on 2-3 beginner projects",
                "Join coding communities and forums"
            ],
            "2": [
                "Master intermediate concepts in your field",
                "Build practical projects to strengthen skills",
                "Contribute to open-source projects",
                "Participate in hackathons or competitions",
                "Network with professionals in your domain"
            ],
            "3": [
                "Learn advanced tools and frameworks",
                "Build portfolio-worthy projects",
                "Start applying for internships",
                "Attend workshops and tech conferences",
                "Mentor junior students in your area",
                "Keep up with industry trends"
            ],
            "4": [
                "Master production-level skills",
                "Build industry-standard projects",
                "Prepare for technical interviews",
                "Complete internships or freelance work",
                "Create a strong portfolio and resume",
                "Apply for full-time positions"
            ]
        }
        
        return generic_steps.get(year, generic_steps["2"])
    
    def generate_roadmap(self, year: str, interest: str, branch: str) -> Dict:
        """
        Main function to generate complete roadmap.
        
        Args:
            year (str): Student's current year (1-4)
            interest (str): Area of interest
            branch (str): Engineering branch
        
        Returns:
            Dict: Complete roadmap with difficulty and steps
        """
        difficulty_level = self.get_difficulty_level(year)
        steps = self.get_roadmap_steps(year, interest, branch)
        
        return {
            "difficulty_level": difficulty_level,
            "steps": steps
        }


def get_roadmap(year: str, interest: str, branch: str) -> Dict:
    """
    Convenience function for generating roadmaps.
    This is the main function that should be called from Flask.
    
    Args:
        year (str): Student's current year (1-4)
        interest (str): Area of interest
        branch (str): Engineering branch
    
    Returns:
        Dict: Roadmap with difficulty_level and steps
    """
    engine = RoadmapEngine()
    return engine.generate_roadmap(year, interest, branch)


# For testing purposes
if __name__ == "__main__":
    # Test the roadmap engine
    test_cases = [
        ("1", "Web Development", "CSE"),
        ("2", "Data Science", "CSE"),
        ("3", "Mobile Development", "IT"),
        ("4", "Web Development", "ECE")
    ]
    
    print("Testing Roadmap Engine\n" + "="*50)
    
    for year, interest, branch in test_cases:
        print(f"\nYear: {year}, Interest: {interest}, Branch: {branch}")
        print("-" * 50)
        
        roadmap = get_roadmap(year, interest, branch)
        
        print(f"Difficulty: {roadmap['difficulty_level']}")
        print("Steps:")
        for i, step in enumerate(roadmap['steps'], 1):
            print(f"  {i}. {step}")