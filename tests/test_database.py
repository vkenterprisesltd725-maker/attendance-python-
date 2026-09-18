import pytest
import sqlite3
import os
from pathlib import Path
from database.database import get_connection, initialize_database, execute_query, fetch_one
from services.student_service import StudentService

# Use an in-memory database or a test file for tests
TEST_DB = "test_student_performance.db"

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    initialize_database(db_path=TEST_DB)
    
    # Overwrite the db_path globally for the service during test by monkeypatch
    # However, since we designed `execute_query` to take db_path, we need to mock it.
    yield
    
    # Teardown
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass # Windows file lock fallback

def test_database_initialization():
    with get_connection(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in cursor.fetchall()]
        assert "users" in tables
        assert "students" in tables
        assert "predictions" in tables
        assert "recommendations" in tables

def test_student_crud(monkeypatch):
    # Mock the default DB_PATH in execute_query, fetch_one, fetch_all
    import database.database as db
    monkeypatch.setattr(db, "DB_PATH", TEST_DB)
    
    student_data = {
        "student_id": "STU9999",
        "name": "Test Student",
        "age": 20,
        "gender": "Male",
        "department": "CSE",
        "semester": 4,
        "attendance": 85.0,
        "internal_marks": 75.0,
        "assignment_marks": 80.0,
        "previous_percentage": 78.0,
        "study_hours": 4.5,
        "assignment_completion": 90.0,
        "participation": 80.0,
        "backlogs": 0,
        "extracurricular": "Yes"
    }

    # 1. Insertion
    success, msg = StudentService.create_student(student_data)
    assert success is True

    # 2. Duplicate handling
    success, msg = StudentService.create_student(student_data)
    assert success is False
    assert "already exists" in msg

    # 3. Retrieval
    student = StudentService.get_student("STU9999")
    assert student is not None
    assert student["name"] == "Test Student"

    # 4. Update
    student_data["name"] = "Updated Name"
    success, msg = StudentService.update_student("STU9999", student_data)
    assert success is True
    student = StudentService.get_student("STU9999")
    assert student["name"] == "Updated Name"

    # 5. Deletion
    success, msg = StudentService.delete_student("STU9999")
    assert success is True
    student = StudentService.get_student("STU9999")
    assert student is None

def test_foreign_keys(monkeypatch):
    import database.database as db
    monkeypatch.setattr(db, "DB_PATH", TEST_DB)
    
    # Try inserting prediction for non-existent student (should fail due to foreign key)
    with pytest.raises(sqlite3.IntegrityError):
        execute_query(
            "INSERT INTO predictions (student_id, predicted_category) VALUES (?, ?)", 
            ("INVALID_ID", "Good"), 
            db_path=TEST_DB
        )
