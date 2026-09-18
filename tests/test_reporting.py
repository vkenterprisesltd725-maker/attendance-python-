import pytest
import os
from pathlib import Path
from database.database import initialize_database
from services.report_service import ReportService
from services.student_service import StudentService

TEST_DB = "test_reporting.db"

@pytest.fixture(autouse=True)
def setup_teardown(monkeypatch):
    import database.database as db
    monkeypatch.setattr(db, "DB_PATH", TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    initialize_database(db_path=TEST_DB)
    
    # Seed
    StudentService.create_student({
        "student_id": "STU9999",
        "name": "Report Test",
        "age": 20,
        "gender": "Female",
        "department": "ECE",
        "semester": 5,
        "attendance": 55.0,
        "internal_marks": 45.0,
        "assignment_marks": 70.0,
        "previous_percentage": 65.0,
        "study_hours": 1.5,
        "assignment_completion": 60.0,
        "participation": 50.0,
        "backlogs": 1,
        "extracurricular": "No"
    })
    
    yield
    
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass

def test_generate_report_success():
    filepath = ReportService.generate_student_report("STU9999")
    assert os.path.exists(filepath)
    assert filepath.endswith("STU9999_performance_report.pdf")
    
    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)

def test_generate_report_invalid_student():
    with pytest.raises(ValueError, match="not found"):
        ReportService.generate_student_report("NON_EXISTENT")
