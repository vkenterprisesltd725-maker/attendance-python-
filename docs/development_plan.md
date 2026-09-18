# Development & Testing Plan

## Phase 1: Project Initialization & Architecture (Completed)
- Directory structure initialized.
- Requirements documented.
- Database and architecture designed.
- Basic configurations set.

## Phase 2: Data Generation & Database Implementation (Completed)
- Implement `schema.sql` and `database.py`.
- Write Python script to generate the synthetic 500-1000 row dataset.
- Implement `student_service.py` to allow basic CRUD and data import.

## Phase 3: Machine Learning Implementation (Completed)
- Data validation and preprocessing (`preprocessing.py`).
- Implement model training (`train_model.py`) with Random Forest/Logistic Regression.
- Model evaluation and persistence.
- Develop `prediction_service.py` and `recommendation_service.py`.

## Phase 4: Risk Engine & Recommendation Integration (Completed)
- Explainable Risk Engine (`risk_service.py`).
- Rule-based recommendations (`recommendation_service.py`).
- Complete `prediction_service.py` pipeline.
- Database persistence for predictions and recommendations.

## Phase 5: GUI Implementation (Completed)
- Develop `CustomTkinter` views.
- Login screen, Dashboard, Data management, and Prediction views.
- Integrate GUI with the service layer.

## Phase 6: Reporting & Analytics (Upcoming)
Execute the testing strategy defined below.

---

## Testing Strategy

### Unit Tests (`pytest`)
- **Validators:** Test that invalid ages, negative marks, or impossible attendance >100% are rejected.
- **Database Operations:** Test that CRUD operations work on an in-memory SQLite DB.
- **Recommendation Engine:** Test that specific risk factors trigger the correct recommendation strings.
- **Prediction Functions:** Verify ML pipeline structure, preprocessing logic, and model load logic without GUI.

### Integration Tests
- **Database + Service Layer:** Ensure `student_service.py` correctly queries and maps database rows into dictionaries/objects.
- **ML + Prediction Service:** Ensure passing a raw student record triggers preprocessing and returns a valid risk score.
- **Report Generation:** Ensure `report_service.py` successfully writes a `.pdf` file to the filesystem.

### End-to-End (Manual/UI Testing)
- Login as Admin.
- Add a new student via the GUI.
- Predict risk for the new student.
- Generate and open the PDF report.
