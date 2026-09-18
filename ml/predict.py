import os
import sys
import pandas as pd
import joblib
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.config import MODELS_DIR

# Global cache for loaded models
_MODELS = {}

def load_model(artifact_name: str):
    '''Loads and caches a model artifact.'''
    if artifact_name not in _MODELS:
        model_path = MODELS_DIR / artifact_name
        if not model_path.exists():
            raise FileNotFoundError(f"Model artifact not found: {model_path}")
        _MODELS[artifact_name] = joblib.load(model_path)
    return _MODELS[artifact_name]

def predict_performance(student_data: dict) -> dict:
    '''Predicts the performance category for a given student record.'''
    model = load_model("performance_model.joblib")
    df = pd.DataFrame([student_data])
    
    prediction = model.predict(df)[0]
    result = {"performance_category": prediction}
    
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(df)[0]
        classes = model.classes_
        result["class_probabilities"] = {str(c): float(p) for c, p in zip(classes, probs)}
        
    return result

def predict_risk(student_data: dict) -> dict:
    '''Predicts the academic risk level for a given student record.'''
    model = load_model("risk_model.joblib")
    df = pd.DataFrame([student_data])
    
    prediction = model.predict(df)[0]
    result = {"risk_level": prediction}
    
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(df)[0]
        classes = model.classes_
        result["class_probabilities"] = {str(c): float(p) for c, p in zip(classes, probs)}
        
    return result

def predict_student(student_data: dict) -> dict:
    '''Runs both performance and risk predictions.'''
    try:
        perf = predict_performance(student_data)
        risk = predict_risk(student_data)
        
        return {
            "performance_category": perf["performance_category"],
            "performance_probabilities": perf.get("class_probabilities", {}),
            "risk_level": risk["risk_level"],
            "risk_probabilities": risk.get("class_probabilities", {})
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Sample usage test
    sample_student = {
        "age": 20, "semester": 4, "attendance": 85.0, "internal_marks": 75.0,
        "assignment_marks": 80.0, "previous_percentage": 78.0, "study_hours": 4.5,
        "assignment_completion": 90.0, "participation": 80.0, "backlogs": 0,
        "gender": "Male", "department": "CSE", "extracurricular": "Yes"
    }
    print(predict_student(sample_student))
