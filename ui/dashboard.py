import customtkinter as ctk
from ui.theme import Theme, get_risk_color
from ui.session import session
from ui.components.stat_card import StatCard
from database.database import fetch_one, fetch_all
from services.student_service import StudentService
from services.prediction_service import PredictionService

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.title = ctk.CTkLabel(self, text="Dashboard", font=Theme.HEADER_FONT)
        self.title.pack(anchor="nw", pady=(0, 20))
        
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)
        
        if session.is_admin():
            self.build_admin_dashboard()
        else:
            self.build_student_dashboard()
            
    def build_admin_dashboard(self):
        # Fetch stats
        total_students = fetch_one("SELECT COUNT(*) as count FROM students")["count"]
        high_risk = fetch_one("SELECT COUNT(*) as count FROM predictions WHERE risk_level = 'High'")["count"]
        med_risk = fetch_one("SELECT COUNT(*) as count FROM predictions WHERE risk_level = 'Medium'")["count"]
        low_risk = fetch_one("SELECT COUNT(*) as count FROM predictions WHERE risk_level = 'Low'")["count"]
        
        c1 = StatCard(self.cards_frame, "Total Students", total_students)
        c1.pack(side="left", fill="x", expand=True, padx=5)
        
        c2 = StatCard(self.cards_frame, "High Risk", high_risk, color=Theme.DANGER)
        c2.pack(side="left", fill="x", expand=True, padx=5)
        
        c3 = StatCard(self.cards_frame, "Medium Risk", med_risk, color=Theme.WARNING)
        c3.pack(side="left", fill="x", expand=True, padx=5)
        
        c4 = StatCard(self.cards_frame, "Low Risk", low_risk, color=Theme.SUCCESS)
        c4.pack(side="left", fill="x", expand=True, padx=5)
        
    def build_student_dashboard(self):
        student_data = StudentService.get_student(session.student_id)
        latest_pred = PredictionService.get_latest_prediction(session.student_id)
        
        # Row 1
        c1 = StatCard(self.cards_frame, "Attendance", f"{student_data['attendance']}%")
        c1.pack(side="left", fill="x", expand=True, padx=5)
        
        c2 = StatCard(self.cards_frame, "Internal Marks", f"{student_data['internal_marks']}%")
        c2.pack(side="left", fill="x", expand=True, padx=5)
        
        c3 = StatCard(self.cards_frame, "Assignment Completion", f"{student_data['assignment_completion']}%")
        c3.pack(side="left", fill="x", expand=True, padx=5)
        
        # Row 2 for predictions if any
        if latest_pred:
            row2 = ctk.CTkFrame(self, fg_color="transparent")
            row2.pack(fill="x", pady=20)
            
            p1 = StatCard(row2, "Performance Category", latest_pred["predicted_category"].upper())
            p1.pack(side="left", fill="x", expand=True, padx=5)
            
            r_level = latest_pred["risk_level"]
            p2 = StatCard(row2, "Risk Level", r_level.upper(), color=get_risk_color(r_level))
            p2.pack(side="left", fill="x", expand=True, padx=5)
            
            p3 = StatCard(row2, "Risk Score", f"{latest_pred['risk_score']} / 100")
            p3.pack(side="left", fill="x", expand=True, padx=5)
