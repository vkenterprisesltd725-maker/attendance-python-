import customtkinter as ctk
from tkinter import messagebox
from ui.theme import Theme
from ui.session import session
from utils.security import verify_password
from database.database import fetch_one

class LoginView(ctk.CTkFrame):
    def __init__(self, master, switch_to_main_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.switch_to_main = switch_to_main_callback
        
        # Center frame
        self.login_frame = ctk.CTkFrame(self, width=400, height=500, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.title_label = ctk.CTkLabel(
            self.login_frame, text="Academic Risk System", font=Theme.HEADER_FONT
        )
        self.title_label.pack(pady=(40, 30))
        
        self.username_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Username / Student ID", width=250, height=40
        )
        self.username_entry.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Password", show="*", width=250, height=40
        )
        self.password_entry.pack(pady=10)
        
        self.login_button = ctk.CTkButton(
            self.login_frame, text="Login", width=250, height=40, font=Theme.TITLE_FONT,
            command=self.handle_login
        )
        self.login_button.pack(pady=30)
        
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter username and password.")
            return
            
        user_record = fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        
        if user_record and verify_password(password, user_record["password_hash"]):
            session.login(username=username, role=user_record["role"], student_id=user_record["student_id"])
            self.switch_to_main()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
