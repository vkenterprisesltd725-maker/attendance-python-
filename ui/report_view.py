import customtkinter as ctk
from ui.theme import Theme

class ReportView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.title = ctk.CTkLabel(self, text="Generate Reports", font=Theme.HEADER_FONT)
        self.title.pack(anchor="nw", pady=(0, 20))
        
        card = ctk.CTkFrame(self, corner_radius=15, width=400, height=200)
        card.pack(pady=50)
        card.pack_propagate(False)
        
        label = ctk.CTkLabel(card, text="Report generation will be enabled in the reporting phase.", font=Theme.NORMAL_FONT, wraplength=350)
        label.place(relx=0.5, rely=0.5, anchor="center")
