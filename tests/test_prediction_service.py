import pytest
import os
from database.database import initialize_database, execute_query
from services.student_service import StudentService
from services.prediction_service import PredictionService

TEST_DB = "test_prediction_integration.db"

@pytest.fixture(autouse=True)
def setup_teardown(monkeypatch):
    import database.database as db
    monkeypatch.setattr(db, "DB_PATH", TEST_DB)
    
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    initialize_database(db_path=TEST_DB)
    
    # Seed a student
    student_data = {
        "student_id": "STU8888",
        "name": "Integration Test",
        "age": 20,
        "gender": "Female",
        "department": "ECE",
        "semester": 5,
        "attendance": 55.0, # Will trigger risk factor
        "internal_marks": 45.0,
        "assignment_marks": 70.0,
        "previous_percentage": 65.0,
        "study_hours": 1.5,
        "assignment_completion": 60.0,
        "participation": 50.0,
        "backlogs": 1,
        "extracurricular": "No"
    }
    succ, m = StudentService.create_student(student_data)
    assert succ, m
    
    yield
    
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass

def test_full_prediction_pipeline():
    # 1. Student data reaches ML pipeline, scores calculated, stored
    success, result, msg = PredictionService.run_prediction_for_student("STU8888")
    
    assert success is True, msg
    
    # Check Structure
    assert result is not None
    assert "performance_category" in result
    assert "risk_level" in result
    assert "risk_score" in result
    assert "risk_factors" in result
    assert "recommendations" in result
    
    # Check Values
    assert result["student_id"] == "STU8888"
    assert result["risk_score"] > 0
    assert len(result["risk_factors"]) > 0
    assert len(result["recommendations"]) > 0
    
    # Check DB persistence (Predictions table)
    history = PredictionService.get_prediction_history("STU8888")
    assert len(history) == 1
    assert history[0]["predicted_category"] == result["performance_category"]
    
    # Check latest prediction
    latest = PredictionService.get_latest_prediction("STU8888")
    assert latest["prediction_id"] == history[0]["prediction_id"]
    
    # Check DB persistence (Recommendations table)
    from services.recommendation_service import RecommendationService
    db_recs = RecommendationService.get_recommendations("STU8888")
    assert len(db_recs) == len(result["recommendations"])

def test_prediction_invalid_student():
    success, result, msg = PredictionService.run_prediction_for_student("NON_EXISTENT")
    assert success is False
    assert result is None
    assert "not found" in msg
