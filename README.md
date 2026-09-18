# Student Performance & Academic Risk Prediction System

## Overview
A comprehensive Python-based desktop application designed to analyze, predict, and mitigate student academic risk. Developed as a final project for an Infosys Springboard Industrial Training Program.

## Problem Statement
Educational institutions often struggle to proactively identify students at risk of academic failure before critical exams. By the time grades are published, interventions are frequently too late. 

## Objectives
1. Provide a centralized interface to manage student academic records.
2. Utilize Machine Learning to predict performance categories and overarching risk levels.
3. Utilize a deterministic Risk Engine to calculate specific Risk Scores and identify actionable factors.
4. Auto-generate personalized academic interventions and professional PDF reports.

## Key Features
- **CustomTkinter GUI**: Modern, responsive Desktop UI with light/dark modes.
- **Machine Learning Integration**: Scikit-Learn based classification models.
- **Rule-based Risk Engine**: Transparent, explainable risk scoring mechanism.
- **Role-Based Access Control**: Secure Admin vs. Student isolated environments.
- **Visual Analytics**: Interactive Matplotlib distributions.
- **ReportLab PDF Generation**: Automated, printable academic profiles.

## Architecture
The application strictly follows an N-Tier architecture:
1. **Presentation Layer**: CustomTkinter UI.
2. **Service Layer**: Business logic (StudentService, PredictionService, ReportService).
3. **Intelligence Layer**: Scikit-learn `.joblib` models and deterministic Risk Engine.
4. **Data Layer**: SQLite Database (`database.py`) with raw SQL queries.

## Technology Stack
- **Language**: Python 3.11+
- **GUI**: CustomTkinter, Tkinter
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn, Joblib
- **Visualization**: Matplotlib
- **Reporting**: ReportLab
- **Database**: SQLite3
- **Testing**: Pytest

## Machine Learning Approach
We evaluate multiple algorithms (Logistic Regression, Decision Tree, Random Forest). Logistic Regression was selected for optimal precision and explainability across our dataset. 

## Risk Engine & Recommendation Engine
The machine-learning model predicts the student's performance category and risk class from academic features, while a separate rule-based risk engine identifies actionable academic risk factors. The Recommendation Engine maps these deterministic factors into high/medium/low priority interventions, avoiding opaque LLM hallucination.

## Dataset
**IMPORTANT: The included dataset is synthetic and is intended for educational/demo purposes.** Model performance should not be interpreted as real-world predictive validity.

## Project Structure
```text
student-performance-risk/
├── app.py                     # Main GUI Entry Point
├── data/                      # Synthetic data generation & CSV
├── database/                  # SQLite schema and operations
├── ml/                        # ML Pipeline & Training scripts
├── models/                    # Pickled .joblib models & metadata
├── services/                  # Core business logic bridging DB, ML, and UI
├── ui/                        # CustomTkinter Views & Components
├── tests/                     # 40+ Pytest suite
├── reports/                   # Generated PDF output directory
├── examples/                  # CLI demo scripts
└── docs/                      # Comprehensive technical documentation
```

## Installation
1. Clone the repository.
2. Ensure Python 3.11+ is installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
Launch the graphical interface:
```bash
python app.py
```

## ML Training
To retrain the machine learning models on a fresh dataset:
```bash
python ml/train_model.py
```

## Demo Credentials
Use the following credentials to explore the presentation flow:

**Admin Access**
- Username: `admin`
- Password: `Admin@123`

**Student Access**
- Username: `STU0001`
- Password: `Student@123`

## Testing
Run the complete regression suite:
```bash
pytest
```

## Screenshots
*(Insert GUI Screenshots Here)*

## Limitations
See `docs/limitations.md`. Predictions support—not replace—academic intervention decisions.

## Future Enhancements
- Cloud deployment via Flask/FastAPI backend.
- Integration with institutional LMS (Learning Management Systems).
- Real-time notification services (Email/SMS) for high-risk flags.

## Author
**3rd-Semester B.Tech CSE Student**
Infosys Springboard Industrial Training Project