import customtkinter as ctk
from ui.theme import Theme
from ui.session import session

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, width=200, corner_radius=0, fg_color=Theme.PRIMARY, **kwargs)
        self.navigate = navigate_callback
        
        # Title
        self.title = ctk.CTkLabel(self, text="Risk System", font=Theme.TITLE_FONT, text_color="white")
        self.title.pack(pady=30, padx=20)
        
        # Nav Buttons
        self.add_nav_button("Dashboard", "dashboard")
        
        if session.is_admin():
            self.add_nav_button("Students", "students")
            self.add_nav_button("Analytics", "analytics")
            self.add_nav_button("Reports", "reports")
        else:
            self.add_nav_button("My Profile", "profile")
            
        # Spacer
        ctk.CTkFrame(self, fg_color="transparent").pack(expand=True, fill="both")
        
        # User Info & Logout
        user_text = f"{session.username} ({session.role.capitalize()})"
        ctk.CTkLabel(self, text=user_text, text_color="white", font=Theme.SMALL_FONT).pack(pady=10)
        
        self.logout_btn = ctk.CTkButton(self, text="Logout", fg_color="transparent", border_width=1, text_color="white", hover_color=Theme.PRIMARY_HOVER, command=lambda: self.navigate("logout"))
        self.logout_btn.pack(pady=20, padx=20)
        
    def add_nav_button(self, text, view_name):
        btn = ctk.CTkButton(self, text=text, fg_color="transparent", text_color="white", hover_color=Theme.PRIMARY_HOVER, anchor="w", font=Theme.NORMAL_FONT, command=lambda: self.navigate(view_name))
        btn.pack(fill="x", pady=5, padx=10)
