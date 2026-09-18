import pandas as pd
import sqlite3
from typing import List, Dict, Tuple
from database.database import execute_query, fetch_one, fetch_all, get_connection
from utils.validators import validate_student_record
from utils.logger import get_logger

logger = get_logger(__name__)

class StudentService:
    @staticmethod
    def create_student(student_data: Dict) -> Tuple[bool, str]:
        is_valid, errors = validate_student_record(student_data)
        if not is_valid:
            return False, "; ".join(errors)
            
        try:
            query = """
                INSERT INTO students (
                    student_id, name, age, gender, department, semester, 
                    attendance, internal_marks, assignment_marks, previous_percentage,
                    study_hours, assignment_completion, participation, backlogs, extracurricular
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                student_data['student_id'], student_data['name'], student_data['age'],
                student_data['gender'], student_data['department'], student_data['semester'],
                student_data['attendance'], student_data['internal_marks'], student_data['assignment_marks'],
                student_data['previous_percentage'], student_data['study_hours'], 
                student_data['assignment_completion'], student_data['participation'], 
                student_data['backlogs'], student_data['extracurricular']
            )
            execute_query(query, params)
            return True, "Student created successfully."
        except sqlite3.IntegrityError:
            return False, f"Student with ID {student_data['student_id']} already exists."
        except Exception as e:
            logger.error(f"Error creating student: {e}")
            return False, str(e)

    @staticmethod
    def get_student(student_id: str) -> Dict:
        query = "SELECT * FROM students WHERE student_id = ?"
        return fetch_one(query, (student_id,))

    @staticmethod
    def get_all_students() -> List[Dict]:
        query = "SELECT * FROM students"
        return fetch_all(query)

    @staticmethod
    def update_student(student_id: str, student_data: Dict) -> Tuple[bool, str]:
        is_valid, errors = validate_student_record(student_data)
        if not is_valid:
            return False, "; ".join(errors)
            
        try:
            query = """
                UPDATE students SET
                    name = ?, age = ?, gender = ?, department = ?, semester = ?, 
                    attendance = ?, internal_marks = ?, assignment_marks = ?, previous_percentage = ?,
                    study_hours = ?, assignment_completion = ?, participation = ?, backlogs = ?, 
                    extracurricular = ?, updated_at = CURRENT_TIMESTAMP
                WHERE student_id = ?
            """
            params = (
                student_data['name'], student_data['age'], student_data['gender'], 
                student_data['department'], student_data['semester'], student_data['attendance'], 
                student_data['internal_marks'], student_data['assignment_marks'], 
                student_data['previous_percentage'], student_data['study_hours'], 
                student_data['assignment_completion'], student_data['participation'], 
                student_data['backlogs'], student_data['extracurricular'], student_id
            )
            execute_query(query, params)
            return True, "Student updated successfully."
        except Exception as e:
            logger.error(f"Error updating student: {e}")
            return False, str(e)

    @staticmethod
    def delete_student(student_id: str) -> Tuple[bool, str]:
        try:
            execute_query("DELETE FROM students WHERE student_id = ?", (student_id,))
            return True, "Student deleted successfully."
        except Exception as e:
            logger.error(f"Error deleting student: {e}")
            return False, str(e)

    @staticmethod
    def import_from_file(file_path: str) -> Tuple[int, int, List[str]]:
        """
        Imports students from a CSV or Excel file.
        Returns: (success_count, fail_count, list_of_errors)
        """
        success_count = 0
        fail_count = 0
        errors = []

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                return 0, 1, ["Unsupported file format. Please use .csv or .xlsx"]
                
            # Basic required columns check
            required_cols = {'student_id', 'name', 'age'}
            if not required_cols.issubset(set(df.columns)):
                return 0, 1, [f"Missing required columns. Expected at least: {required_cols}"]

            # Fill NaNs where appropriate to avoid insert errors
            df = df.where(pd.notnull(df), None)

            for index, row in df.iterrows():
                student_dict = row.to_dict()
                
                # Check for existing
                if StudentService.get_student(student_dict['student_id']):
                    errors.append(f"Row {index+1}: Student {student_dict['student_id']} already exists.")
                    fail_count += 1
                    continue
                    
                success, msg = StudentService.create_student(student_dict)
                if success:
                    success_count += 1
                else:
                    errors.append(f"Row {index+1} ({student_dict.get('student_id')}): {msg}")
                    fail_count += 1
                    
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            errors.append(f"File reading error: {str(e)}")
            fail_count += 1

        return success_count, fail_count, errors
