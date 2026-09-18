from typing import Dict, Any
from database.database import fetch_one

class DataQualityService:
    @staticmethod
    def get_quality_summary() -> Dict[str, Any]:
        stats = {}
        
        total = fetch_one("SELECT COUNT(*) as c FROM students")
        stats['total_records'] = total['c'] if total else 0
        
        # In a real system, we might look for NULLs. Here we just query for it.
        missing_att = fetch_one("SELECT COUNT(*) as c FROM students WHERE attendance IS NULL OR internal_marks IS NULL")
        stats['missing_values'] = missing_att['c'] if missing_att else 0
        
        duplicates = fetch_one("SELECT COUNT(*) as c FROM (SELECT student_id FROM students GROUP BY student_id HAVING COUNT(*) > 1)")
        stats['duplicates'] = duplicates['c'] if duplicates else 0
        
        stats['valid_records'] = stats['total_records'] - stats['missing_values'] - stats['duplicates']
        
        return stats
