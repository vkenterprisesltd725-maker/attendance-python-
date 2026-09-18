from typing import Dict, List, Any
from database.database import execute_query, fetch_all

class RecommendationService:
    @staticmethod
    def generate_recommendations(student_data: Dict[str, Any], risk_factors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generates personalized, rule-based recommendations.
        Does NOT use AI/LLMs. Purely deterministic based on provided risk factors.
        """
        recommendations = []
        
        # If no risk factors, return standard encouragement
        if not risk_factors:
            return [{
                "recommendation": "No major academic risk factors were detected from the provided indicators. Continue maintaining your current academic habits.",
                "priority": "Low"
            }]
        
        # Map existing factors to personalized recommendations
        for factor in risk_factors:
            f_name = factor["factor"]
            f_val = factor["current_value"]
            
            if f_name == "Attendance":
                recommendations.append({
                    "recommendation": f"Your attendance is {f_val}%. Improve class attendance and maintain at least 75% attendance where institution policy requires it.",
                    "priority": "High"
                })
            elif f_name == "Internal Marks":
                recommendations.append({
                    "recommendation": f"Your internal marks are {f_val}%. Focus on core subjects and prepare systematically for upcoming internal assessments.",
                    "priority": "High"
                })
            elif f_name == "Assignment Completion":
                recommendations.append({
                    "recommendation": f"Your assignment completion rate is {f_val}%. Complete pending assignments and establish a weekly submission schedule.",
                    "priority": "Medium"
                })
            elif f_name == "Previous Percentage":
                recommendations.append({
                    "recommendation": f"Your previous semester percentage was {f_val}%. Review previous-semester weak subjects and strengthen foundational concepts.",
                    "priority": "Medium"
                })
            elif f_name == "Study Hours":
                recommendations.append({
                    "recommendation": f"You reported {f_val} study hours per day. Increase focused daily study time gradually and follow a consistent study schedule.",
                    "priority": "Medium"
                })
            elif f_name == "Backlogs":
                recommendations.append({
                    "recommendation": f"You currently have {f_val} backlogs. Create a backlog-clearing plan and prioritize previously incomplete subjects.",
                    "priority": "High"
                })
            elif f_name == "Participation":
                recommendations.append({
                    "recommendation": f"Your participation score is {f_val}%. Increase participation in classes, discussions, and academic activities.",
                    "priority": "Low"
                })
                
        # Sort recommendations by priority: High -> Medium -> Low
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return recommendations

    @staticmethod
    def save_recommendations(student_id: str, recommendations: List[Dict[str, Any]]):
        """Persists generated recommendations to the database."""
        # Clear existing to avoid infinite clutter, or simply append. The prompt says: 
        # "Do not store duplicate recommendations unnecessarily."
        # We'll clear the old ones for this student and insert the new ones.
        execute_query("DELETE FROM recommendations WHERE student_id = ?", (student_id,))
        
        for rec in recommendations:
            query = """
                INSERT INTO recommendations (student_id, recommendation, priority)
                VALUES (?, ?, ?)
            """
            execute_query(query, (student_id, rec["recommendation"], rec["priority"]))

    @staticmethod
    def get_recommendations(student_id: str) -> List[Dict]:
        """Retrieves recommendations for a specific student."""
        query = "SELECT * FROM recommendations WHERE student_id = ? ORDER BY created_at DESC"
        return fetch_all(query, (student_id,))
