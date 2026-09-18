import os
import customtkinter as ctk
from tkinter import messagebox
from ui.theme import Theme
from services.report_service import ReportService
from services.student_service import StudentService

class ReportView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.title = ctk.CTkLabel(self, text="Generate Reports", font=Theme.HEADER_FONT)
        self.title.pack(anchor="nw", pady=(0, 20))
        
        card = ctk.CTkFrame(self, corner_radius=15, width=500, height=300)
        card.pack(pady=50)
        card.pack_propagate(False)
        
        title_lbl = ctk.CTkLabel(card, text="Student Performance Report", font=Theme.TITLE_FONT)
        title_lbl.pack(pady=(30, 20))
        
        self.student_entry = ctk.CTkEntry(card, placeholder_text="Enter Student ID (e.g. STU0001)", width=250)
        self.student_entry.pack(pady=10)
        
        gen_btn = ctk.CTkButton(card, text="Generate PDF Report", command=self.generate_report)
        gen_btn.pack(pady=20)
        
        self.status_lbl = ctk.CTkLabel(card, text="", text_color=Theme.SUCCESS)
        self.status_lbl.pack()
        
    def generate_report(self):
        student_id = self.student_entry.get().strip()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return
            
        student = StudentService.get_student(student_id)
        if not student:
            messagebox.showerror("Error", f"Student {student_id} not found.")
            return
            
        try:
            self.status_lbl.configure(text="Generating...", text_color=Theme.TEXT_LIGHT)
            self.update() # flush UI
            
            filepath = ReportService.generate_student_report(student_id)
            self.status_lbl.configure(text=f"Success! Saved to:\n{filepath}", text_color=Theme.SUCCESS)
            
            # Offer to open the report
            if messagebox.askyesno("Report Generated", "PDF generated successfully. Do you want to open it?"):
                if os.name == 'nt':
                    os.startfile(filepath)
                else:
                    import subprocess
                    subprocess.call(['open', filepath])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")
            self.status_lbl.configure(text="Generation failed.", text_color=Theme.DANGER)
