# System Requirements Engineering

## 1. PROJECT OVERVIEW
This project is an **Academic performance analytics + machine-learning prediction + academic risk identification + personalized recommendations** system. It is designed to assist administrators and teachers in monitoring student performance, analyzing academic data, and proactively identifying students at risk of academic failure. Unlike a basic student management system that only stores information, this application uses machine learning to provide actionable insights and personalized recommendations.

## 2. PROBLEM STATEMENT
Educational institutions collect vast amounts of academic data, but this information is often merely stored and rarely analyzed systematically. Consequently, it is difficult to proactively identify students who may require academic support until they have already performed poorly or failed a course. There is a critical need for an automated system to analyze existing data and flag academic risk factors early.

## 3. OBJECTIVES
1. Store student academic information securely.
2. Import academic datasets via CSV/Excel.
3. Validate and preprocess imported data.
4. Analyze student performance metrics.
5. Train classification models to predict performance.
6. Predict performance categories (Excellent, Good, Average, Needs Improvement).
7. Identify academic risk levels (Low, Medium, High).
8. Explain important risk factors affecting the student.
9. Generate personalized recommendations based on identified risks.
10. Provide visual analytics for instructors.
11. Generate PDF student reports.
12. Provide role-based access for Administrators/Teachers and Students.

## 4. SCOPE
### Included
- Student management & Academic data management
- Data import & preprocessing
- ML classification & Risk analysis
- Recommendations
- Dashboard & Reports
- Local Database (SQLite)
- Authentication & Testing

### Not included initially
- Mobile application & Cloud deployment
- Real-time attendance hardware or Face recognition
- Production institutional integration (e.g., LMS/ERP)
- Medical/psychological assessments
- Automated high-stakes decisions

## 5. USER ROLES
### Administrator/Teacher
**Capabilities:** Login, Manage students, Import data, View analytics, Run predictions, View risk analysis, Generate reports, Export data, Manage ML model.

### Student
**Capabilities:** Login, View own profile, View academic performance, View prediction, View risk factors, View recommendations, View reports.

## 6. FUNCTIONAL REQUIREMENTS
- **FR-001 — User Authentication**: Role-based login.
- **FR-002 — Student Creation**: Add single student records.
- **FR-003 — Student Update**: Modify existing student records.
- **FR-004 — Student Deletion**: Remove students.
- **FR-005 — Student Search**: Search by ID or Name.
- **FR-006 — CSV Import**: Batch load student data via CSV.
- **FR-007 — Excel Import**: Batch load student data via Excel.
- **FR-008 — Data Validation**: Reject malformed inputs during manual entry or bulk import.
- **FR-009 — Model Prediction**: Run ML predictions on one or more students.
- **FR-010 — Risk Classification**: Classify risk level based on ML probability/rules.
- **FR-011 — Recommendation Generation**: Assign actionable advice to students.
- **FR-012 — Analytics**: Display aggregate metrics on the dashboard.
- **FR-013 — Report Generation**: Export student risk profiles as PDFs.
- **FR-014 — Data Export**: Export table views to CSV/Excel.
- **FR-015 — Prediction History**: Retain past predictions in the database.

## 7. NON-FUNCTIONAL REQUIREMENTS
- **Usability**: Simple desktop GUI (Tkinter/CustomTkinter).
- **Reliability**: Graceful handling of corrupted CSVs.
- **Maintainability**: Modular Python project structure.
- **Performance**: Predict < 5 seconds per batch of 50 students.
- **Security**: Passwords hashed, no plain text storage.
- **Portability**: Runs on Windows using a local virtual environment.
- **Scalability**: Can handle up to 10,000 local student records efficiently.
- **Error handling**: Descriptive UI messages, background logging.
- **Testability**: Isolated service layer suitable for `pytest`.

## 8. INPUT FEATURES
### Categorical features
- **Gender**: Contextual demographic analysis.
- **Department**: Variations in scoring by department.
- **Extracurricular Participation**: Impact of external activities.

### Numerical features
- **Age**: Basic demographic.
- **Semester**: Academic progression stage.
- **Attendance %**: Often highly correlated with success.
- **Internal Marks**: Current semester checkpoint.
- **Assignment Marks**: Current continuous assessment.
- **Previous Semester %**: Baseline past performance.
- **Study Hours/Day**: Self-reported effort.
- **Assignment Completion %**: Reliability metric.
- **Class Participation %**: Engagement metric.
- **Previous Backlogs**: Key risk indicator.

## 9. TARGET VARIABLES
### Primary Target: Performance Category
Generated dynamically in synthetic data based on a weighted sum of numerical features, binned into:
- Excellent
- Good
- Average
- Needs Improvement

### Secondary Target: Academic Risk
Derived from the Performance Category or raw score:
- Low
- Medium
- High

## 10. RISK SCORING
An explainable scoring methodology will assign weights to features (e.g., Attendance < 75% adds risk, Previous Backlogs > 0 adds significant risk).
*Disclaimer: Risk score is an academic analytics indicator, not a diagnosis or guaranteed future outcome.*

## 11. MACHINE LEARNING REQUIREMENTS
Candidates to evaluate:
- **Logistic Regression**: Baseline model. Highly interpretable, fast. May underfit complex relationships.
- **Decision Tree**: Highly interpretable rules. Prone to overfitting.
- **Random Forest**: Expected to perform best. Handles non-linear relationships well, offers feature importance. Less interpretable than a single tree.

## 12. DATA PREPROCESSING
Using `sklearn` Pipeline & ColumnTransformer for:
1. Data validation and type checking.
2. Missing-value imputation (mean/median for numerical, mode for categorical).
3. Duplicate handling.
4. Outlier checking (IQR).
5. Categorical encoding (OneHotEncoding).
6. Numerical scaling (StandardScaler/MinMaxScaler).
7. Train/test split.
8. Reproducibility (random_state).
9. Pipeline persistence (saving via `joblib`).

## 13. MODEL EVALUATION
Metrics to record during Phase 2 training:
- Accuracy
- Precision (macro/weighted)
- Recall (macro/weighted)
- F1-score (macro/weighted)
- Confusion matrix

## 18. GUI REQUIREMENTS (Planned)
1. Login
2. Admin Dashboard
3. Student Dashboard
4. Student Management
5. Add Student
6. Edit Student
7. Import Data
8. Prediction
9. Risk Analysis
10. Analytics
11. Reports
12. Model Evaluation
13. Settings

## 19. LIVE DEMO REQUIREMENTS (Planned Flow)
1. Login -> 2. Show dashboard -> 3. Add student -> 4. Enter academic data -> 5. Generate prediction -> 6. Display risk -> 7. Show risk factors -> 8. Show recommendations -> 9. Show class analytics -> 10. Generate report.

## 20. SAMPLE DATA STRATEGY
Synthetic dataset (500–1000 records). Uses realistic correlations (e.g., lower attendance = lower marks = higher risk) without a trivial deterministic formula. Random noise will be injected to ensure the ML model must learn patterns rather than simple linear rules.

## 22. SECURITY REQUIREMENTS
- Password hashing (e.g., `bcrypt` or `werkzeug.security`).
- Role-based access checks on UI screens.
- Parameterized SQL via sqlite3 to prevent injection.
- Input validation on all UI fields.
- No secrets in source code.
- No sensitive data in logs.

## 23. FUTURE SCOPE
Web interface, REST API, Mobile application, Cloud database, Real institutional data, Automated attendance integration, LMS integration.

## 24. LIMITATIONS
- Synthetic training data restricts real-world validity out-of-the-box.
- Limited feature set (e.g., missing socio-economic factors).
- Prediction depends strictly on data quality.
- Model performance depends on training data.
- Not a guaranteed prediction of student outcomes; not for high-stakes decisions.
