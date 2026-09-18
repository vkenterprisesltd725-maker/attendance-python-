import sqlite3
from typing import Dict, Tuple, Optional, Any
from database.database import execute_query, fetch_all, fetch_one
from services.student_service import StudentService
from services.risk_service import RiskService
from services.recommendation_service import RecommendationService
from ml.predict import predict_student
from utils.logger import get_logger

logger = get_logger(__name__)

class PredictionService:
    @staticmethod
    def predict_student_data(student_data: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Core function that orchestrates the entire intelligence pipeline.
        Runs ML models, calculates risk score, finds factors, and generates recommendations.
        '''
        # 1. Prepare data for ML (Drop db metadata)
        ml_input = dict(student_data)
        for key in ['created_at', 'updated_at', 'student_id', 'name']:
            ml_input.pop(key, None)
            
        # 2. Run ML Models
        ml_prediction = predict_student(ml_input)
        if "error" in ml_prediction:
            return {"error": ml_prediction["error"]}
            
        # 3. Calculate Explainable Risk Score
        risk_score = RiskService.calculate_risk_score(student_data)
        
        # 4. Identify Risk Factors
        risk_factors = RiskService.identify_risk_factors(student_data)
        
        # 5. Generate Recommendations
        recommendations = RecommendationService.generate_recommendations(student_data, risk_factors)
        
        # Combine into a structured result
        result = {
            "student_id": student_data.get('student_id', 'UNKNOWN'),
            "performance_category": ml_prediction.get('performance_category'),
            "performance_probabilities": ml_prediction.get('performance_probabilities', {}),
            "risk_level": ml_prediction.get('risk_level'),
            "risk_probabilities": ml_prediction.get('risk_probabilities', {}),
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "model_name": "Logistic Regression" # From Phase 3 selections
        }
        
        return result

    @staticmethod
    def run_prediction_for_student(student_id: str) -> Tuple[bool, Optional[Dict], str]:
        '''
        Fetches student data, runs intelligence pipeline, and saves history.
        Returns: (success, prediction_results, message)
        '''
        student_data = StudentService.get_student(student_id)
        if not student_data:
            return False, None, f"Student {student_id} not found."
            
        try:
            # Run Intelligence Pipeline
            prediction = PredictionService.predict_student_data(student_data)
            
            if "error" in prediction:
                logger.error(f"Prediction failed for {student_id}: {prediction['error']}")
                return False, None, prediction["error"]
                
            # 6. Database Persistence - Save Prediction
            query = """
                INSERT INTO predictions (
                    student_id, predicted_category, risk_level, risk_score, model_name
                ) VALUES (?, ?, ?, ?, ?)
            """
            params = (
                student_id, 
                prediction['performance_category'], 
                prediction['risk_level'],
                prediction['risk_score'],
                prediction['model_name']
            )
            execute_query(query, params)
            
            # 7. Database Persistence - Save Recommendations
            RecommendationService.save_recommendations(student_id, prediction['recommendations'])
            
            return True, prediction, "Prediction generated successfully."
            
        except Exception as e:
            logger.error(f"Error running prediction service: {e}")
            return False, None, str(e)

    @staticmethod
    def get_prediction_history(student_id: str) -> list[Dict]:
        '''Retrieves past predictions for a specific student.'''
        query = "SELECT * FROM predictions WHERE student_id = ? ORDER BY prediction_date DESC"
        return fetch_all(query, (student_id,))

    @staticmethod
    def get_latest_prediction(student_id: str) -> Optional[Dict]:
        '''Retrieves the most recent prediction for a specific student.'''
        query = "SELECT * FROM predictions WHERE student_id = ? ORDER BY prediction_date DESC LIMIT 1"
        return fetch_one(query, (student_id,))
