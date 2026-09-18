import customtkinter as ctk
from ui.theme import Theme

class StatCard(ctk.CTkFrame):
    def __init__(self, master, title: str, value: str, color: str = Theme.PRIMARY, **kwargs):
        super().__init__(master, corner_radius=10, fg_color=("gray90", "gray16"), **kwargs)
        
        self.title_label = ctk.CTkLabel(
            self, text=title, font=Theme.NORMAL_FONT, text_color=("gray30", "gray70")
        )
        self.title_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        self.value_label = ctk.CTkLabel(
            self, text=str(value), font=(Theme.FONT_FAMILY, 28, "bold"), text_color=color
        )
        self.value_label.pack(pady=(0, 15), padx=20, anchor="w")

    def update_value(self, new_value: str, new_color: str = None):
        self.value_label.configure(text=str(new_value))
        if new_color:
            self.value_label.configure(text_color=new_color)
