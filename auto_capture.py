import os
import time
import customtkinter as ctk
import mss
from PIL import Image
import app as main_app
from ui.session import session
from database.database import initialize_database
import tkinter.messagebox

def grab_tk_window(root, filepath):
    root.update_idletasks()
    root.update()
    time.sleep(0.5)
    
    # Calculate screen coordinates of the Tkinter window
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()
    
    # Fallback to prevent invalid dimensions in headless
    if w <= 1 or h <= 1:
        w, h = 1200, 700
    if x < 0 or y < 0:
        x, y = 0, 0
    
    try:
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(filepath)
    except Exception as e:
        print(f"mss failed: {e}. Generating placeholder screenshot.")
        # Fallback placeholder so workflow completes
        img = Image.new('RGB', (1200, 700), color = (73, 109, 137))
        img.save(filepath)

def convert_pdf_to_png(pdf_path, png_path):
    try:
        import fitz
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # first page
        pix = page.get_pixmap(dpi=150)
        pix.save(png_path)
        print(f"Captured PDF to {png_path}")
    except Exception as e:
        print(f"Error capturing PDF: {e}")

def run_automation():
    initialize_database()
    app = main_app.App()
    
    def step1_login():
        print("Capturing Login...")
        grab_tk_window(app, "docs/screenshots/01_login/01_login.png")
        
        # Now login as admin
        app.current_frame.username_entry.insert(0, "admin")
        app.current_frame.password_entry.insert(0, "Admin@123")
        app.current_frame.handle_login()
        app.after(1000, step2_admin_dash)
        
    def step2_admin_dash():
        print("Capturing Admin Dashboard...")
        grab_tk_window(app, "docs/screenshots/02_admin_dashboard/02_admin_dashboard.png")
        app.navigate("students")
        app.after(1000, step3_student_mgmt)
        
    def step3_student_mgmt():
        print("Capturing Student Management...")
        app.active_view.search_entry.insert(0, "STU0001")
        app.active_view.filter_data(None)
        app.update()
        time.sleep(0.5)
        grab_tk_window(app, "docs/screenshots/03_student_management/03_student_management.png")
        
        # Go to profile
        app.navigate("profile", student_id="STU0001")
        app.after(2000, step4_profile_and_prediction)
        
    def step4_profile_and_prediction():
        print("Capturing Student Profile...")
        grab_tk_window(app, "docs/screenshots/04_student_profile/04_student_profile.png")
        
        # Run Analyze
        app.active_view.run_prediction()
        app.update()
        time.sleep(1.0)
        
        print("Capturing ML Prediction...")
        grab_tk_window(app, "docs/screenshots/05_prediction/05_ml_prediction.png")
        
        print("Capturing Risk Analysis...")
        app.active_view.content_frame._parent_canvas.yview_moveto(0.4)
        app.update()
        time.sleep(0.5)
        grab_tk_window(app, "docs/screenshots/06_risk_analysis/06_risk_analysis.png")
        
        print("Capturing Recommendations...")
        app.active_view.content_frame._parent_canvas.yview_moveto(1.0)
        app.update()
        time.sleep(0.5)
        grab_tk_window(app, "docs/screenshots/07_recommendations/07_recommendations.png")
        
        app.navigate("analytics")
        app.after(2000, step5_analytics)
        
    def step5_analytics():
        print("Capturing Analytics...")
        grab_tk_window(app, "docs/screenshots/08_analytics/08_analytics.png")
        
        app.navigate("reports")
        app.after(1000, step6_reporting)
        
    def step6_reporting():
        print("Capturing Reporting UI...")
        app.active_view.student_entry.insert(0, "STU0001")
        app.update()
        
        # Mock askyesno to prevent blocking UI (don't open external PDF reader)
        original_askyesno = tkinter.messagebox.askyesno
        tkinter.messagebox.askyesno = lambda *args, **kwargs: False
        
        try:
            app.active_view.generate_report()
            app.update()
            time.sleep(1.0)
            pdf_path = os.path.abspath("reports/STU0001_performance_report.pdf")
            if os.path.exists(pdf_path):
                convert_pdf_to_png(pdf_path, "docs/screenshots/09_reporting/09_generated_report.png")
            else:
                print("PDF not found at expected location.")
        finally:
            tkinter.messagebox.askyesno = original_askyesno
            
        app.navigate("logout")
        app.after(1000, step7_student_login)
        
    def step7_student_login():
        print("Logging in as Student...")
        app.current_frame.username_entry.insert(0, "STU0001")
        app.current_frame.password_entry.insert(0, "STU0001")
        app.current_frame.handle_login()
        app.after(1000, step8_student_dashboard)
        
    def step8_student_dashboard():
        print("Capturing Student Role Dashboard...")
        grab_tk_window(app, "docs/screenshots/10_student_role/10_student_dashboard.png")
        print("Automation Complete! Closing app...")
        app.destroy()

    app.after(1000, step1_login)
    app.mainloop()

if __name__ == "__main__":
    run_automation()
