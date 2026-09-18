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
### 📌 Implemented (Phases 1, 2, 3)
- Project Architecture & Initialization
- Requirements & Database Design
- ML Strategy & Configuration Boilerplate
- Synthetic Dataset Generation (1000 records)
- SQLite Database Implementation & Access Layer
- Student Service (CRUD & CSV Import)
- Password Security (PBKDF2 HMAC)
- Machine Learning Pipeline (Training, Preprocessing, Evaluation)
- Scikit-Learn Model Persistence (.joblib)
- Prediction Service Integration
- Explainable Risk Engine (Score & Factor Detection)
- Rule-based Recommendation Engine
- CustomTkinter Desktop GUI
- Matplotlib Analytics Dashboard
- Role-based Access Control (Admin/Student)

### ⏳ Planned (Upcoming Phases)
- **Dashboard**: Visual analytics and statistics.
- **Reporting Engine**: PDF report generation via ReportLab.
- **GUI Construction**: Tkinter / CustomTkinter interface.

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
1. Clone the repository.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment (`.venv\Scripts\activate` on Windows).
4. Install dependencies: `pip install -r requirements.txt`
5. Generate Data: `python data/generate_dataset.py`
6. Initialize Database: `python database/seed.py`
7. Train ML Models: `python ml/train_model.py`

## Running the Application
*(Currently only runs the boilerplate initialization)*
```bash
python app.py
```

### Machine Learning Workflow
The system predicts Performance Category and Risk Level independently.
- To train models and output confusion matrices:
  ```bash
  python ml/train_model.py
  ```
- To evaluate existing artifacts:
  ```bash
  python ml/evaluate_model.py
  ```

## Demo Credentials
*(For demonstration purposes only)*
- **Admin**: `admin` / `Admin@123`
- **Student**: `STU0001` / `Student@123`

## Dataset
A synthetic dataset of 1,000 records containing realistic correlations (e.g., lower attendance generally equates to higher academic risk) was generated to train the model and populate the demo database. See `data/README.md`.

## Testing
Unit and integration tests have been developed using `pytest`.
```bash
pytest
```

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

## Intelligent Prediction Workflow
The system employs a multi-step intelligence pipeline to move from raw data to actionable insights:
1. **Student Data**: Base features loaded from SQLite.
2. **ML Prediction**: Scikit-Learn models predict categorical risk and performance.
3. **Risk Score**: A deterministic risk engine calculates a 0-100 score based on weighted academic thresholds.
4. **Risk Factors**: Extracts exact thresholds violated (e.g. Attendance < 75%).
5. **Recommendations**: Generates personalized, prioritized interventions.
6. **Prediction History**: The entire structured result is persisted in the database for longitudinal tracking.