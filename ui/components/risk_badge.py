import customtkinter as ctk
from ui.theme import Theme, get_risk_color

class RiskBadge(ctk.CTkFrame):
    def __init__(self, master, risk_level: str, **kwargs):
        color = get_risk_color(risk_level)
        super().__init__(master, fg_color=color, corner_radius=15, **kwargs)
        
        self.label = ctk.CTkLabel(
            self, text=risk_level.upper(), font=Theme.NORMAL_FONT, text_color="white"
        )
        self.label.pack(padx=15, pady=5)
        
    def update_risk(self, risk_level: str):
        color = get_risk_color(risk_level)
        self.configure(fg_color=color)
        self.label.configure(text=risk_level.upper())
