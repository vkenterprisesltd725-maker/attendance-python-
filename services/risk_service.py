from typing import Dict, List, Any

# Configurable Risk Thresholds (can be moved to config.py if desired)
RISK_LEVEL_THRESHOLDS = {
    "Low": (0, 33),
    "Medium": (34, 66),
    "High": (67, 100)
}

class RiskService:
    @staticmethod
    def calculate_risk_score(student_data: Dict[str, Any]) -> float:
        """
        Calculates an explainable academic risk score (0-100).
        0 = lowest academic risk, 100 = highest academic risk.
        """
        score = 0.0
        
        # 1. Attendance (20% weight) -> risk is (100 - attendance) * 0.20
        attendance = float(student_data.get('attendance', 100))
        score += max(0, 100 - attendance) * 0.20
        
        # 2. Internal Marks (25% weight) -> risk is (100 - marks) * 0.25
        internal_marks = float(student_data.get('internal_marks', 100))
        score += max(0, 100 - internal_marks) * 0.25
        
        # 3. Assignment Completion (15% weight) -> risk is (100 - completion) * 0.15
        assignment_completion = float(student_data.get('assignment_completion', 100))
        score += max(0, 100 - assignment_completion) * 0.15
        
        # 4. Previous Percentage (15% weight) -> risk is (100 - prev) * 0.15
        previous_percentage = float(student_data.get('previous_percentage', 100))
        score += max(0, 100 - previous_percentage) * 0.15
        
        # 5. Study Hours (10% weight) -> normalized against 10 hours max
        study_hours = float(student_data.get('study_hours', 10))
        study_hours_norm = min(study_hours, 10.0) / 10.0 * 100
        score += max(0, 100 - study_hours_norm) * 0.10
        
        # 6. Backlogs (10% weight) -> normalized against 5 max
        backlogs = int(student_data.get('backlogs', 0))
        backlogs_norm = min(backlogs, 5) / 5.0 * 100
        score += backlogs_norm * 0.10
        
        # 7. Participation (5% weight) -> risk is (100 - participation) * 0.05
        participation = float(student_data.get('participation', 100))
        score += max(0, 100 - participation) * 0.05
        
        return round(min(100.0, score), 2)

    @staticmethod
    def get_risk_level(score: float) -> str:
        """Maps numeric score to Risk Level."""
        if score <= RISK_LEVEL_THRESHOLDS["Low"][1]:
            return "Low"
        elif score <= RISK_LEVEL_THRESHOLDS["Medium"][1]:
            return "Medium"
        else:
            return "High"

    @staticmethod
    def identify_risk_factors(student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyzes student data to generate explainable risk factors.
        Returns a list of dictionaries detailing the factors.
        """
        factors = []
        
        attendance = float(student_data.get('attendance', 100))
        if attendance < 75:
            severity = "High" if attendance < 60 else "Medium"
            factors.append({
                "factor": "Attendance",
                "severity": severity,
                "current_value": attendance,
                "threshold": 75,
                "explanation": "Attendance is below the recommended threshold."
            })
            
        internal_marks = float(student_data.get('internal_marks', 100))
        if internal_marks < 50:
            severity = "High" if internal_marks < 40 else "Medium"
            factors.append({
                "factor": "Internal Marks",
                "severity": severity,
                "current_value": internal_marks,
                "threshold": 50,
                "explanation": "Internal assessment performance is low."
            })
            
        assignment_completion = float(student_data.get('assignment_completion', 100))
        if assignment_completion < 70:
            factors.append({
                "factor": "Assignment Completion",
                "severity": "Medium",
                "current_value": assignment_completion,
                "threshold": 70,
                "explanation": "Assignment completion is below the recommended level."
            })
            
        previous_percentage = float(student_data.get('previous_percentage', 100))
        if previous_percentage < 60:
            factors.append({
                "factor": "Previous Percentage",
                "severity": "Medium",
                "current_value": previous_percentage,
                "threshold": 60,
                "explanation": "Previous academic performance indicates an area requiring attention."
            })
            
        study_hours = float(student_data.get('study_hours', 10))
        if study_hours < 2:
            factors.append({
                "factor": "Study Hours",
                "severity": "Medium",
                "current_value": study_hours,
                "threshold": 2,
                "explanation": "Daily study time is relatively low."
            })
            
        backlogs = int(student_data.get('backlogs', 0))
        if backlogs >= 2:
            severity = "High" if backlogs >= 3 else "Medium"
            factors.append({
                "factor": "Backlogs",
                "severity": severity,
                "current_value": backlogs,
                "threshold": 2,
                "explanation": "Multiple backlogs may increase academic risk."
            })
            
        participation = float(student_data.get('participation', 100))
        if participation < 40:
            factors.append({
                "factor": "Participation",
                "severity": "Low",
                "current_value": participation,
                "threshold": 40,
                "explanation": "Class participation is relatively low."
            })
            
        # Sort factors by severity: High -> Medium -> Low
        severity_order = {"High": 0, "Medium": 1, "Low": 2}
        factors.sort(key=lambda x: severity_order.get(x["severity"], 3))
        
        return factors
