import re

def validate_student_id(student_id: str) -> bool:
    """Validates student ID format (e.g., STU0001)."""
    if not student_id: return False
    return bool(re.match(r'^STU\d{4}$', student_id))

def validate_age(age: int) -> bool:
    """Validates age is within a reasonable student range."""
    try:
        return 15 <= int(age) <= 60
    except (ValueError, TypeError):
        return False

def validate_percentage(val: float) -> bool:
    """Validates a percentage value is between 0 and 100."""
    try:
        return 0.0 <= float(val) <= 100.0
    except (ValueError, TypeError):
        return False

def validate_study_hours(val: float) -> bool:
    """Validates study hours are realistic (0-24)."""
    try:
        return 0.0 <= float(val) <= 24.0
    except (ValueError, TypeError):
        return False

def validate_semester(val: int) -> bool:
    """Validates semester is between 1 and 8."""
    try:
        return 1 <= int(val) <= 8
    except (ValueError, TypeError):
        return False

def validate_backlogs(val: int) -> bool:
    """Validates backlogs are positive integers."""
    try:
        return int(val) >= 0
    except (ValueError, TypeError):
        return False

def validate_student_record(record: dict) -> tuple[bool, list[str]]:
    """
    Validates a complete student record dictionary.
    Returns (is_valid, list_of_errors).
    """
    errors = []
    
    if not validate_student_id(record.get('student_id', '')):
        errors.append("Invalid student ID format.")
        
    if not record.get('name') or not str(record.get('name')).strip():
        errors.append("Name is required.")
        
    if not validate_age(record.get('age')):
        errors.append("Age must be between 15 and 60.")
        
    if not validate_semester(record.get('semester')):
        errors.append("Semester must be between 1 and 8.")
        
    for pct_field in ['attendance', 'internal_marks', 'assignment_marks', 'previous_percentage', 'assignment_completion', 'participation']:
        if not validate_percentage(record.get(pct_field)):
            errors.append(f"{pct_field} must be between 0 and 100.")
            
    if not validate_study_hours(record.get('study_hours')):
        errors.append("Study hours must be between 0 and 24.")
        
    if not validate_backlogs(record.get('backlogs')):
        errors.append("Backlogs must be 0 or greater.")
        
    return len(errors) == 0, errors
