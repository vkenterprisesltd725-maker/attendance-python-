from typing import Dict, List, Any
from database.database import fetch_all, fetch_one

class AnalyticsService:
    @staticmethod
    def get_overview_stats() -> Dict[str, Any]:
        """Retrieves high-level summary statistics for the dashboard."""
        stats = {}
        
        # Total Students
        row = fetch_one("SELECT COUNT(student_id) as c, AVG(attendance) as avg_att, AVG(internal_marks) as avg_int, AVG(previous_percentage) as avg_prev, AVG(study_hours) as avg_sh, SUM(backlogs) as sum_b FROM students")
        if row:
            stats['total_students'] = row.get('c', 0)
            stats['avg_attendance'] = round(row.get('avg_att', 0) or 0, 1)
            stats['avg_internal_marks'] = round(row.get('avg_int', 0) or 0, 1)
            stats['avg_previous_percentage'] = round(row.get('avg_prev', 0) or 0, 1)
            stats['avg_study_hours'] = round(row.get('avg_sh', 0) or 0, 1)
            stats['total_backlogs'] = row.get('sum_b', 0) or 0
        else:
            stats.update({'total_students': 0, 'avg_attendance': 0, 'avg_internal_marks': 0, 'avg_previous_percentage': 0, 'avg_study_hours': 0, 'total_backlogs': 0})
            
        # Risk Counts (latest predictions only per student, assuming our demo mainly holds 1 per student or we just do simple count)
        # For simplicity and speed, we will count all predictions or we could get latest. 
        # Using all predictions since this is an educational demo.
        high_risk = fetch_one("SELECT COUNT(*) as c FROM predictions WHERE risk_level = 'High'")
        med_risk = fetch_one("SELECT COUNT(*) as c FROM predictions WHERE risk_level = 'Medium'")
        low_risk = fetch_one("SELECT COUNT(*) as c FROM predictions WHERE risk_level = 'Low'")
        
        stats['high_risk_count'] = high_risk['c'] if high_risk else 0
        stats['medium_risk_count'] = med_risk['c'] if med_risk else 0
        stats['low_risk_count'] = low_risk['c'] if low_risk else 0
        
        return stats

    @staticmethod
    def get_risk_distribution() -> List[Dict]:
        return fetch_all("SELECT risk_level, COUNT(*) as count FROM predictions GROUP BY risk_level")

    @staticmethod
    def get_performance_distribution() -> List[Dict]:
        return fetch_all("SELECT predicted_category, COUNT(*) as count FROM predictions GROUP BY predicted_category")

    @staticmethod
    def get_attendance_data() -> List[float]:
        rows = fetch_all("SELECT attendance FROM students WHERE attendance IS NOT NULL")
        return [float(r['attendance']) for r in rows]

    @staticmethod
    def get_backlog_data() -> List[Dict]:
        return fetch_all("SELECT backlogs, COUNT(*) as count FROM students GROUP BY backlogs ORDER BY backlogs ASC")
