import os
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from services.student_service import StudentService
from services.prediction_service import PredictionService
from services.recommendation_service import RecommendationService

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

class ReportService:
    @staticmethod
    def generate_student_report(student_id: str) -> str:
        """
        Generates a professional PDF report for a given student.
        Returns the absolute filepath to the generated PDF.
        """
        student = StudentService.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found.")

        prediction = PredictionService.get_latest_prediction(student_id)
        recommendations = RecommendationService.get_recommendations(student_id)
        history = PredictionService.get_prediction_history(student_id)

        filename = f"{student_id}_performance_report.pdf"
        filepath = REPORTS_DIR / filename
        
        doc = SimpleDocTemplate(str(filepath), pagesize=letter,
                                rightMargin=40, leftMargin=40,
                                topMargin=40, bottomMargin=40)
        
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = 1 # Center
        h2_style = styles['Heading2']
        normal_style = styles['Normal']
        
        story = []
        
        # --- TITLE ---
        story.append(Paragraph("STUDENT PERFORMANCE & ACADEMIC RISK REPORT", title_style))
        story.append(Spacer(1, 20))
        
        # --- STUDENT INFO ---
        student_data = [
            ["Student ID", student['student_id'], "Department", student['department']],
            ["Name", student['name'], "Semester", str(student['semester'])]
        ]
        t = Table(student_data, colWidths=[100, 150, 100, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
            ('BACKGROUND', (2,0), (2,-1), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # --- ACADEMIC SUMMARY ---
        story.append(Paragraph("ACADEMIC SUMMARY", h2_style))
        acad_data = [
            ["Attendance", f"{student['attendance']}%", "Study Hours", str(student['study_hours'])],
            ["Internal Marks", f"{student['internal_marks']}%", "Backlogs", str(student['backlogs'])],
            ["Prev. Percentage", f"{student['previous_percentage']}%", "Assignment Comp.", f"{student['assignment_completion']}%"]
        ]
        t2 = Table(acad_data, colWidths=[120, 130, 120, 130])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.whitesmoke),
            ('BACKGROUND', (2,0), (2,-1), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t2)
        story.append(Spacer(1, 20))
        
        if prediction:
            # --- ML PREDICTION ---
            story.append(Paragraph("ML PREDICTION & RISK SCORE", h2_style))
            pred_data = [
                ["Performance Category", str(prediction['predicted_category']).upper()],
                ["Risk Level", str(prediction['risk_level']).upper()],
                ["Risk Score", f"{prediction['risk_score']} / 100"]
            ]
            t3 = Table(pred_data, colWidths=[200, 300])
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), colors.aliceblue),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(t3)
            story.append(Spacer(1, 20))
            
            # --- RECOMMENDATIONS ---
            story.append(Paragraph("PERSONALIZED RECOMMENDATIONS", h2_style))
            if recommendations:
                rec_data = [["Priority", "Recommendation"]]
                for r in recommendations:
                    # Using Paragraph inside table for text wrap
                    rec_text = Paragraph(r['recommendation'], normal_style)
                    rec_data.append([r['priority'].upper(), rec_text])
                    
                t4 = Table(rec_data, colWidths=[80, 420])
                t4.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ]))
                story.append(t4)
            else:
                story.append(Paragraph("No major risk recommendations available.", normal_style))
            story.append(Spacer(1, 20))
            
        # --- SYSTEM INFO ---
        story.append(Spacer(1, 30))
        story.append(Paragraph("SYSTEM INFORMATION", h2_style))
        story.append(Paragraph("Model: Logistic Regression (Scikit-Learn)", normal_style))
        story.append(Paragraph("The machine-learning model predicts the student's performance category and risk class from academic features, while a separate rule-based risk engine identifies actionable academic risk factors.", normal_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        
        doc.build(story)
        return str(filepath)
