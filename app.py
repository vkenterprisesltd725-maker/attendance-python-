import sys
import customtkinter as ctk
from ui.theme import Theme
from ui.session import session
from ui.login import LoginView
from ui.components.sidebar import Sidebar
from ui.dashboard import DashboardView
from ui.student_view import StudentView
from ui.prediction_view import PredictionView
from ui.analytics_view import AnalyticsView
from ui.report_view import ReportView
from database.database import initialize_database

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Performance & Academic Risk Prediction System")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        self.current_frame = None
        self.show_login()
        
    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        session.clear()
        self.current_frame = LoginView(self, self.show_main_layout)
        self.current_frame.pack(fill="both", expand=True)
        
    def show_main_layout(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(self.current_frame, self.navigate)
        self.sidebar.pack(side="left", fill="y")
        
        # Main Content Area
        self.content_area = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        self.content_area.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        
        self.active_view = None
        self.navigate("dashboard")
        
    def navigate(self, view_name: str, **kwargs):
        if view_name == "logout":
            self.show_login()
            return
            
        if self.active_view:
            self.active_view.destroy()
            
        if view_name == "dashboard":
            self.active_view = DashboardView(self.content_area)
        elif view_name == "students" and session.is_admin():
            self.active_view = StudentView(self.content_area, lambda sid: self.navigate("profile", student_id=sid))
        elif view_name == "profile":
            sid = kwargs.get("student_id")
            self.active_view = PredictionView(self.content_area, student_id=sid)
        elif view_name == "analytics" and session.is_admin():
            self.active_view = AnalyticsView(self.content_area)
        elif view_name == "reports" and session.is_admin():
            self.active_view = ReportView(self.content_area)
            
        if self.active_view:
            self.active_view.pack(fill="both", expand=True)

def main():
    initialize_database()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
