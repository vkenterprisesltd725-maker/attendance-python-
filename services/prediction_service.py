import sqlite3
from typing import Dict, Tuple, Optional
from database.database import execute_query, fetch_one, fetch_all
from services.student_service import StudentService
from ml.predict import predict_student
from utils.logger import get_logger

logger = get_logger(__name__)

class PredictionService:
    @staticmethod
    def run_prediction_for_student(student_id: str) -> Tuple[bool, Optional[Dict], str]:
        '''
        Fetches student data, runs ML models, and saves the prediction history.
        Returns: (success, prediction_results, message)
        '''
        student_data = StudentService.get_student(student_id)
        if not student_data:
            return False, None, f"Student {student_id} not found."
            
        try:
            # Drop unnecessary DB metadata that shouldn't go to ML model
            ml_input = dict(student_data)
            for key in ['created_at', 'updated_at', 'student_id', 'name']:
                ml_input.pop(key, None)
                
            prediction = predict_student(ml_input)
            
            if "error" in prediction:
                logger.error(f"Prediction failed for {student_id}: {prediction['error']}")
                return False, None, prediction["error"]
                
            # Construct a safe model name/version reference
            # For simplicity, we just label it 'Random Forest' or 'v1.0'
            model_name = "Ensemble_v1.0" 
            
            query = \"\"\"
                INSERT INTO predictions (
                    student_id, predicted_category, risk_level, model_name
                ) VALUES (?, ?, ?, ?)
            \"\"\"
            params = (
                student_id, 
                prediction['performance_category'], 
                prediction['risk_level'],
                model_name
            )
            execute_query(query, params)
            
            return True, prediction, "Prediction generated successfully."
            
        except Exception as e:
            logger.error(f"Error running prediction service: {e}")
            return False, None, str(e)

    @staticmethod
    def get_prediction_history(student_id: str) -> list[Dict]:
        '''Retrieves past predictions for a specific student.'''
        query = "SELECT * FROM predictions WHERE student_id = ? ORDER BY prediction_date DESC"
        return fetch_all(query, (student_id,))
