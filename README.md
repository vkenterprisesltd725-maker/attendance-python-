# Student Performance & Academic Risk Prediction System

## Overview
The **Student Performance & Academic Risk Prediction System** is a Python-based desktop application designed to help educational institutions monitor academic progress and proactively identify students at risk of underperforming. It combines traditional student data management with machine learning to offer predictive analytics and personalized recommendations.

*Note: This is an Infosys Springboard Industrial Training Project (3rd Semester B.Tech CSE).*

## Problem Statement
While institutions collect vast amounts of academic data, it is rarely analyzed systematically in real time. Consequently, students requiring academic support are often identified only after they have failed a course. This project solves this by analyzing continuous assessment data, attendance, and historical performance to flag academic risk early.

## Objectives
1. Store and manage student academic information.
2. Import datasets via CSV/Excel.
3. Predict performance categories using Machine Learning.
4. Identify academic risk levels and explain risk factors.
5. Provide actionable recommendations.
6. Generate PDF reports for students and administrators.

## Features
### 📌 Implemented (Phase 1)
- Project Architecture & Initialization
- Requirements & Database Design
- ML Strategy & Configuration Boilerplate

### ⏳ Planned (Upcoming Phases)
- **Authentication**: Role-based access (Admin, Student).
- **Dashboard**: Visual analytics and statistics.
- **Student Management**: CRUD operations for student records.
- **Predictive Engine**: Scikit-Learn based classification.
- **Reporting Engine**: PDF report generation via ReportLab.

## Technology Stack
- **Language**: Python 3.11+
- **GUI**: CustomTkinter / Tkinter
- **Database**: SQLite3
- **Data & ML**: Pandas, NumPy, Scikit-Learn
- **Visualization**: Matplotlib, Seaborn
- **Reporting**: ReportLab
- **Testing**: Pytest

## Architecture
This application follows a strict N-Tier (Layered) Architecture:
1. **Presentation Layer**: CustomTkinter GUI.
2. **Service Layer**: Pure Python business logic orchestrating Data and ML.
3. **Data Access Layer**: SQLite database integration.
4. **ML Layer**: Scikit-Learn pipeline for training and inference.

See `docs/architecture.md` for full details.

## Project Structure
```text
student-performance-risk/
├── app.py                 # Application entry point
├── config/                # Centralized configurations
├── data/                  # CSV/Excel datasets
├── database/              # SQLite DB and Schema
├── docs/                  # Architecture & Requirements documentation
├── ml/                    # Machine Learning pipeline and scripts
├── models/                # Saved joblib model artifacts
├── reports/               # Generated PDF reports
├── services/              # Business logic layer
├── tests/                 # Pytest unit and integration tests
├── ui/                    # CustomTkinter GUI views
└── utils/                 # Helpers, validators, and loggers
```

## ML Approach
A supervised learning approach utilizing classification algorithms (e.g., Random Forest or Logistic Regression) to categorize student performance based on numerical (attendance, marks, backlogs) and categorical (department, gender) features. The complete pipeline utilizes `sklearn.pipeline.Pipeline` to ensure preprocessing steps are perfectly reproducible during UI inference. See `docs/ml_pipeline.md`.

## Database
A local SQLite database utilizing multiple normalized tables: `users`, `students`, `predictions`, and `recommendations`. See `docs/database.md` for the Entity-Relationship breakdown.

## Installation
*(Instructions for future implementation)*
1. Clone the repository.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment (`.venv\Scripts\activate` on Windows).
4. Install dependencies: `pip install -r requirements.txt`

## Running the Application
*(Currently only runs the boilerplate initialization)*
```bash
python app.py
```

## Dataset
*(Planned)* A synthetic dataset of 500-1000 records containing realistic correlations (e.g., lower attendance generally equates to higher academic risk) will be used to train the model.

## Testing
Unit and integration tests will be developed using `pytest`.

## Future Scope
- Web Interface & REST API.
- Cloud database deployment.
- Real institutional data integration.
- Automated attendance tracking integration.

## Limitations
- Predictions are based on synthetic training data and are restricted by the feature set.
- This is an academic analytics indicator, **not a guaranteed prediction**, and should not be used for high-stakes academic decisions without human review.

## Author
Developed as a 3rd-Semester B.Tech CSE Industrial Training Project.
