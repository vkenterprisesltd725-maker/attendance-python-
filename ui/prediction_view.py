import customtkinter as ctk
from tkinter import messagebox
from ui.theme import Theme
from ui.session import session
from ui.components.risk_badge import RiskBadge
from services.student_service import StudentService
from services.prediction_service import PredictionService

class PredictionView(ctk.CTkFrame):
    def __init__(self, master, student_id: str = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.student_id = student_id if student_id else session.student_id
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.title = ctk.CTkLabel(self.header_frame, text=f"Student Profile & Prediction - {self.student_id}", font=Theme.HEADER_FONT)
        self.title.pack(side="left")
        
        if session.is_admin():
            self.analyze_btn = ctk.CTkButton(self.header_frame, text="Analyze Student", command=self.run_prediction)
            self.analyze_btn.pack(side="right")
            
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        
        self.load_data()
        
    def load_data(self):
        # Clear existing
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        student_data = StudentService.get_student(self.student_id)
        if not student_data:
            ctk.CTkLabel(self.content_frame, text="Student data not found.").pack()
            return
            
        # Basic Info
        info_frame = ctk.CTkFrame(self.content_frame)
        info_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(info_frame, text=f"Name: {student_data['name']} | Dept: {student_data['department']} | Sem: {student_data['semester']}", font=Theme.TITLE_FONT).pack(padx=20, pady=10, anchor="w")
        
        # Latest Prediction
        latest = PredictionService.get_latest_prediction(self.student_id)
        if latest:
            pred_frame = ctk.CTkFrame(self.content_frame)
            pred_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(pred_frame, text="Current Prediction", font=Theme.TITLE_FONT).pack(padx=20, pady=(10,5), anchor="w")
            
            row = ctk.CTkFrame(pred_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(row, text=f"Performance: {latest['predicted_category'].upper()}", font=Theme.NORMAL_FONT).pack(side="left", padx=(0,20))
            ctk.CTkLabel(row, text=f"Risk Score: {latest['risk_score']}/100", font=Theme.NORMAL_FONT).pack(side="left", padx=20)
            RiskBadge(row, latest['risk_level']).pack(side="left", padx=20)
            
            # Fetch Recommendations
            from services.recommendation_service import RecommendationService
            recs = RecommendationService.get_recommendations(self.student_id)
            if recs:
                ctk.CTkLabel(pred_frame, text="Recommendations", font=Theme.TITLE_FONT).pack(padx=20, pady=(15,5), anchor="w")
                for r in recs:
                    rec_text = f"[{r['priority'].upper()}] {r['recommendation']}"
                    color = Theme.DANGER if r['priority'] == 'High' else (Theme.WARNING if r['priority'] == 'Medium' else Theme.TEXT_LIGHT)
                    ctk.CTkLabel(pred_frame, text=rec_text, text_color=color, wraplength=800, justify="left").pack(padx=30, pady=2, anchor="w")
        else:
            ctk.CTkLabel(self.content_frame, text="No predictions generated yet.").pack(pady=20)
            
        # --- SYSTEM INFO DISCLAIMER ---
        disclaimer = "System Information:\nModel: Logistic Regression (Scikit-Learn)\nThe machine-learning model predicts the student's performance category and risk class from academic features, while a separate rule-based risk engine identifies actionable academic risk factors."
        ctk.CTkLabel(self.content_frame, text=disclaimer, font=("Segoe UI", 11, "italic"), text_color="gray50", wraplength=800, justify="left").pack(padx=20, pady=30, anchor="w")
            
    def run_prediction(self):
        success, result, msg = PredictionService.run_prediction_for_student(self.student_id)
        if success:
            self.load_data()
        else:
            messagebox.showerror("Prediction Error", msg)
