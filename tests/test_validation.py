import pytest
from utils.validators import (
    validate_student_id, validate_age, validate_percentage,
    validate_study_hours, validate_semester, validate_student_record
)

def test_validate_student_id():
    assert validate_student_id("STU0001") is True
    assert validate_student_id("STU9999") is True
    assert validate_student_id("ST123") is False  # Invalid format
    assert validate_student_id("STU00001") is False # Too long
    assert validate_student_id("stu0001") is False # Lowercase

def test_validate_age():
    assert validate_age(20) is True
    assert validate_age(15) is True
    assert validate_age(60) is True
    assert validate_age(14) is False
    assert validate_age(61) is False
    assert validate_age("abc") is False

def test_validate_percentage():
    assert validate_percentage(0) is True
    assert validate_percentage(100) is True
    assert validate_percentage(85.5) is True
    assert validate_percentage(-1) is False
    assert validate_percentage(100.1) is False
    assert validate_percentage("abc") is False

def test_validate_study_hours():
    assert validate_study_hours(0) is True
    assert validate_study_hours(12.5) is True
    assert validate_study_hours(24) is True
    assert validate_study_hours(-1) is False
    assert validate_study_hours(25) is False

def test_validate_semester():
    assert validate_semester(1) is True
    assert validate_semester(8) is True
    assert validate_semester(0) is False
    assert validate_semester(9) is False

def test_validate_full_record():
    valid_record = {
        "student_id": "STU1234",
        "name": "Jane Doe",
        "age": 21,
        "gender": "Female",
        "department": "IT",
        "semester": 6,
        "attendance": 90.0,
        "internal_marks": 85.0,
        "assignment_marks": 88.0,
        "previous_percentage": 82.0,
        "study_hours": 3.5,
        "assignment_completion": 95.0,
        "participation": 80.0,
        "backlogs": 0,
        "extracurricular": "Yes"
    }
    
    is_valid, errors = validate_student_record(valid_record)
    assert is_valid is True
    assert len(errors) == 0
    
    invalid_record = valid_record.copy()
    invalid_record["attendance"] = 150.0  # Invalid
    invalid_record["age"] = 10           # Invalid
    
    is_valid, errors = validate_student_record(invalid_record)
    assert is_valid is False
    assert len(errors) == 2
