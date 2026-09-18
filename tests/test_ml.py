import pytest
import pandas as pd
from pathlib import Path

# Add project root to sys.path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from ml.preprocessing import get_preprocessor, NUMERICAL_FEATURES, CATEGORICAL_FEATURES
from ml.train_model import load_data
from ml.predict import predict_student
from config.config import DATA_DIR, MODELS_DIR

def test_dataset_loading():
    df = load_data(DATA_DIR / "sample_students.csv")
    assert not df.empty
    assert 'performance_category' in df.columns
    assert 'risk_level' in df.columns

def test_data_leakage():
    # Targets should not be in the feature lists
    assert 'performance_category' not in NUMERICAL_FEATURES
    assert 'performance_category' not in CATEGORICAL_FEATURES
    assert 'risk_level' not in NUMERICAL_FEATURES
    assert 'risk_level' not in CATEGORICAL_FEATURES
    
    # ID columns should not be features
    assert 'student_id' not in NUMERICAL_FEATURES
    assert 'student_id' not in CATEGORICAL_FEATURES

def test_preprocessing():
    df = load_data(DATA_DIR / "sample_students.csv")
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    
    preprocessor = get_preprocessor()
    X_transformed = preprocessor.fit_transform(X)
    
    # Check that transformation occurred without errors and returned an array
    assert X_transformed is not None
    assert len(X_transformed) == len(X)
    # Check that output features are more than input due to OneHotEncoding
    assert X_transformed.shape[1] > len(CATEGORICAL_FEATURES) + len(NUMERICAL_FEATURES)

def test_predict_student():
    # Only run if models exist
    if not (MODELS_DIR / "performance_model.joblib").exists():
        pytest.skip("Models not trained yet")
        
    sample_student = {
        "age": 20, "semester": 4, "attendance": 85.0, "internal_marks": 75.0,
        "assignment_marks": 80.0, "previous_percentage": 78.0, "study_hours": 4.5,
        "assignment_completion": 90.0, "participation": 80.0, "backlogs": 0,
        "gender": "Male", "department": "CSE", "extracurricular": "Yes"
    }
    
    result = predict_student(sample_student)
    
    assert "error" not in result
    assert "performance_category" in result
    assert "risk_level" in result
    assert result["performance_category"] in ["Excellent", "Good", "Average", "Needs Improvement"]
    assert result["risk_level"] in ["Low", "Medium", "High"]

def test_predict_student_unknown_category():
    if not (MODELS_DIR / "performance_model.joblib").exists():
        pytest.skip("Models not trained yet")
        
    # Department is 'UNKNOWN_DEPT', OneHotEncoder should ignore it
    sample_student = {
        "age": 20, "semester": 4, "attendance": 85.0, "internal_marks": 75.0,
        "assignment_marks": 80.0, "previous_percentage": 78.0, "study_hours": 4.5,
        "assignment_completion": 90.0, "participation": 80.0, "backlogs": 0,
        "gender": "Male", "department": "UNKNOWN_DEPT", "extracurricular": "Yes"
    }
    
    result = predict_student(sample_student)
    assert "error" not in result
