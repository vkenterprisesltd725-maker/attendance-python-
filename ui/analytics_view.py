import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.theme import Theme
from database.database import fetch_all

class AnalyticsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.title = ctk.CTkLabel(self, text="Analytics Dashboard", font=Theme.HEADER_FONT)
        self.title.pack(anchor="nw", pady=(0, 20))
        
        self.chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_frame.pack(fill="both", expand=True)
        
        self.load_charts()
        
    def load_charts(self):
        # Fetch Prediction Distribution
        data = fetch_all("SELECT risk_level, COUNT(*) as count FROM predictions GROUP BY risk_level")
        if not data:
            ctk.CTkLabel(self.chart_frame, text="Insufficient data for analysis.").pack()
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Risk Pie Chart
        labels = [d['risk_level'] for d in data]
        sizes = [d['count'] for d in data]
        colors = [Theme.DANGER if l == 'High' else (Theme.WARNING if l == 'Medium' else Theme.SUCCESS) for l in labels]
        
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title("Academic Risk Distribution")
        
        # Performance Bar Chart
        perf_data = fetch_all("SELECT predicted_category, COUNT(*) as count FROM predictions GROUP BY predicted_category")
        perf_labels = [d['predicted_category'] for d in perf_data]
        perf_sizes = [d['count'] for d in perf_data]
        
        ax2.bar(perf_labels, perf_sizes, color=Theme.PRIMARY)
        ax2.set_title("Performance Category Distribution")
        ax2.tick_params(axis='x', rotation=45)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
