import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox
from ui.theme import Theme
from services.student_service import StudentService

class StudentView(ctk.CTkFrame):
    def __init__(self, master, switch_to_profile, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.switch_to_profile = switch_to_profile
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.title = ctk.CTkLabel(self.header_frame, text="Student Management", font=Theme.HEADER_FONT)
        self.title.pack(side="left")
        
        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Search ID or Name...")
        self.search_entry.pack(side="left", padx=20)
        self.search_entry.bind("<KeyRelease>", self.filter_data)
        
        self.view_btn = ctk.CTkButton(self.header_frame, text="View Profile", command=self.view_profile)
        self.view_btn.pack(side="right")
        
        # Table Frame
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True)
        
        # Treeview Configuration
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=Theme.CARD_BG_LIGHT, foreground=Theme.TEXT_LIGHT, rowheight=30, fieldbackground=Theme.CARD_BG_LIGHT)
        style.map('Treeview', background=[('selected', Theme.PRIMARY)])
        
        columns = ("id", "name", "dept", "sem", "attendance", "marks", "backlogs")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="Student ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("dept", text="Department")
        self.tree.heading("sem", text="Semester")
        self.tree.heading("attendance", text="Attendance %")
        self.tree.heading("marks", text="Internal Marks %")
        self.tree.heading("backlogs", text="Backlogs")
        
        self.tree.column("id", width=100)
        self.tree.column("name", width=200)
        
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.all_students = []
        self.load_data()
        
    def load_data(self):
        self.all_students = StudentService.get_all_students()
        self.populate_tree(self.all_students)
        
    def populate_tree(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for s in data:
            self.tree.insert("", "end", values=(s['student_id'], s['name'], s['department'], s['semester'], s['attendance'], s['internal_marks'], s['backlogs']))

    def filter_data(self, event):
        query = self.search_entry.get().lower()
        filtered = [s for s in self.all_students if query in s['student_id'].lower() or query in s['name'].lower()]
        self.populate_tree(filtered)
        
    def view_profile(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student.")
            return
        
        student_id = self.tree.item(selected[0])['values'][0]
        self.switch_to_profile(student_id)
