import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from services.prediction_service import PredictionService

def run_demo():
    print("========================================")
    print(" STUDENT PERFORMANCE ANALYSIS DEMO")
    print("========================================")
    
    student_id = "STU0001"
    
    print(f"\\nLoading data for Student ID: {student_id}...")
    success, result, msg = PredictionService.run_prediction_for_student(student_id)
    
    if not success:
        print(f"ERROR: {msg}")
        return
        
    print("\\n========================================")
    print(" STUDENT PERFORMANCE ANALYSIS")
    print("========================================")
    print(f"\\nStudent ID: {result['student_id']}")
    
    print(f"\\nPerformance Prediction:")
    print(f"{result['performance_category'].upper()}")
    if result.get("performance_probabilities"):
        probs = result["performance_probabilities"]
        print(f"  (Probabilities: {', '.join([f'{k}: {v:.2f}' for k, v in probs.items()])})")
    
    print(f"\\nML Risk Prediction:")
    print(f"{result['risk_level'].upper()}")
    if result.get("risk_probabilities"):
        probs = result["risk_probabilities"]
        print(f"  (Probabilities: {', '.join([f'{k}: {v:.2f}' for k, v in probs.items()])})")
        
    print(f"\\nAcademic Risk Score:")
    print(f"{result['risk_score']} / 100")
    
    print(f"\\nRisk Factors:")
    if not result['risk_factors']:
        print("- None")
    for factor in result['risk_factors']:
        print(f"- {factor['factor']}: {factor['current_value']}")
        print(f"  Severity: {factor['severity']}")
        print(f"  Reason: {factor['explanation']}")
        
    print(f"\\nRecommendations:")
    for idx, rec in enumerate(result['recommendations'], 1):
        print(f"{idx}. {rec['recommendation']}")
        print(f"   (Priority: {rec['priority']})")
        
    print(f"\\nModel:")
    print(f"{result['model_name']}")
    print("========================================")
    print("\\nPrediction successfully stored in database.")

if __name__ == "__main__":
    run_demo()
