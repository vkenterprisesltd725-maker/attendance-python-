import pytest
from services.risk_service import RiskService
from services.recommendation_service import RecommendationService

def test_recommendation_generation_no_risk():
    factors = []
    recs = RecommendationService.generate_recommendations({}, factors)
    assert len(recs) == 1
    assert "No major academic risk factors" in recs[0]["recommendation"]
    assert recs[0]["priority"] == "Low"

def test_recommendation_prioritization():
    student_data = {
        "attendance": 50, # High priority rec
        "internal_marks": 80, 
        "assignment_completion": 60, # Medium priority rec
        "previous_percentage": 90, 
        "study_hours": 3, 
        "backlogs": 0, 
        "participation": 30 # Low priority rec
    }
    
    factors = RiskService.identify_risk_factors(student_data)
    recs = RecommendationService.generate_recommendations(student_data, factors)
    
    assert len(recs) == 3
    assert "attendance" in recs[0]["recommendation"].lower()
    assert recs[0]["priority"] == "High"
    
    assert "assignment" in recs[1]["recommendation"].lower()
    assert recs[1]["priority"] == "Medium"
    
    assert "participation" in recs[2]["recommendation"].lower()
    assert recs[2]["priority"] == "Low"

def test_recommendation_personalization():
    student_data = {"attendance": 62, "backlogs": 3}
    factors = RiskService.identify_risk_factors(student_data)
    recs = RecommendationService.generate_recommendations(student_data, factors)
    
    assert any("62" in r["recommendation"] for r in recs)
    assert any("3 backlogs" in r["recommendation"] for r in recs)
