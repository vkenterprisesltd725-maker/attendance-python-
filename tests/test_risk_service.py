import pytest
from services.risk_service import RiskService

def test_risk_score_low_risk_student():
    student_data = {
        "attendance": 95,
        "internal_marks": 90,
        "assignment_completion": 90,
        "previous_percentage": 85,
        "study_hours": 6, # 60% of 10
        "backlogs": 0,
        "participation": 80
    }
    
    score = RiskService.calculate_risk_score(student_data)
    # Expected:
    # Att: (100-95)*0.2 = 1.0
    # Int: (100-90)*0.25 = 2.5
    # Ass: (100-90)*0.15 = 1.5
    # Pre: (100-85)*0.15 = 2.25
    # Stu: (100-60)*0.10 = 4.0
    # Bac: 0*0.10 = 0.0
    # Par: (100-80)*0.05 = 1.0
    # Total: 12.25
    assert 10 <= score <= 15
    assert RiskService.get_risk_level(score) == "Low"

def test_risk_score_high_risk_student():
    student_data = {
        "attendance": 40,
        "internal_marks": 30,
        "assignment_completion": 40,
        "previous_percentage": 45,
        "study_hours": 1, 
        "backlogs": 4,
        "participation": 20
    }
    
    score = RiskService.calculate_risk_score(student_data)
    assert score > 66
    assert RiskService.get_risk_level(score) == "High"

def test_risk_boundaries():
    assert RiskService.get_risk_level(33) == "Low"
    assert RiskService.get_risk_level(34) == "Medium"
    assert RiskService.get_risk_level(66) == "Medium"
    assert RiskService.get_risk_level(67) == "High"

def test_risk_factors_identification():
    student_data = {
        "attendance": 50, # High severity (<60)
        "internal_marks": 45, # Medium severity (<50 but not <40)
        "assignment_completion": 80, # Fine
        "previous_percentage": 90, # Fine
        "study_hours": 3, # Fine
        "backlogs": 0, # Fine
        "participation": 30 # Low severity (<40)
    }
    
    factors = RiskService.identify_risk_factors(student_data)
    
    assert len(factors) == 3
    
    # Check ordering (High -> Medium -> Low)
    assert factors[0]["factor"] == "Attendance"
    assert factors[0]["severity"] == "High"
    
    assert factors[1]["factor"] == "Internal Marks"
    assert factors[1]["severity"] == "Medium"
    
    assert factors[2]["factor"] == "Participation"
    assert factors[2]["severity"] == "Low"

def test_missing_values_default_safely():
    # If a student is completely empty, it shouldn't crash
    score = RiskService.calculate_risk_score({})
    assert score is not None
