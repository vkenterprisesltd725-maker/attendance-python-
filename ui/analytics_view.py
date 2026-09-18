import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.theme import Theme
from services.analytics_service import AnalyticsService

class AnalyticsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.title = ctk.CTkLabel(self, text="Analytics Dashboard", font=Theme.HEADER_FONT)
        self.title.pack(anchor="nw", pady=(0, 20))
        
        self.chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_frame.pack(fill="both", expand=True)
        
        self.load_charts()
        
    def load_charts(self):
        risk_data = AnalyticsService.get_risk_distribution()
        perf_data = AnalyticsService.get_performance_distribution()
        att_data = AnalyticsService.get_attendance_data()
        backlog_data = AnalyticsService.get_backlog_data()
        
        if not risk_data and not perf_data and not att_data:
            ctk.CTkLabel(self.chart_frame, text="No sufficient data available.").pack()
            return
            
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        
        # 1. Risk Pie Chart
        if risk_data:
            labels = [d['risk_level'] for d in risk_data]
            sizes = [d['count'] for d in risk_data]
            colors = [Theme.DANGER if l == 'High' else (Theme.WARNING if l == 'Medium' else Theme.SUCCESS) for l in labels]
            axs[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            axs[0, 0].set_title("Academic Risk Distribution")
        else:
            axs[0, 0].text(0.5, 0.5, "No Data", ha='center')
        
        # 2. Performance Bar Chart
        if perf_data:
            perf_labels = [d['predicted_category'] for d in perf_data]
            perf_sizes = [d['count'] for d in perf_data]
            axs[0, 1].bar(perf_labels, perf_sizes, color=Theme.PRIMARY)
            axs[0, 1].set_title("Performance Distribution")
            axs[0, 1].tick_params(axis='x', rotation=15)
        else:
            axs[0, 1].text(0.5, 0.5, "No Data", ha='center')
            
        # 3. Attendance Histogram
        if att_data:
            axs[1, 0].hist(att_data, bins=10, color='skyblue', edgecolor='black')
            axs[1, 0].set_title("Attendance Distribution")
            axs[1, 0].set_xlabel("Attendance %")
            axs[1, 0].set_ylabel("Students")
        else:
            axs[1, 0].text(0.5, 0.5, "No Data", ha='center')
            
        # 4. Backlog Bar Chart
        if backlog_data:
            b_labels = [str(d['backlogs']) for d in backlog_data]
            b_sizes = [d['count'] for d in backlog_data]
            axs[1, 1].bar(b_labels, b_sizes, color='coral', edgecolor='black')
            axs[1, 1].set_title("Backlog Distribution")
            axs[1, 1].set_xlabel("Number of Backlogs")
            axs[1, 1].set_ylabel("Students")
        else:
            axs[1, 1].text(0.5, 0.5, "No Data", ha='center')
            
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
