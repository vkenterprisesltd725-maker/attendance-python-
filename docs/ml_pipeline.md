# Machine Learning Pipeline Design

## 1. Goal
Train a classification model to predict a student's `Performance Category` and derive an `Academic Risk` score based on demographic and academic features.

## 2. Pipeline Architecture
The pipeline relies heavily on `scikit-learn`'s `Pipeline` and `ColumnTransformer` to ensure data leakage is avoided and transformations are reproducible between training and inference.

### Step 2.1: Data Ingestion
- Read `synthetic_students.csv` into a Pandas DataFrame.
- Separate `X` (features) and `y` (target variable).

### Step 2.2: Preprocessing
**Categorical Features:** (e.g., Gender, Department, Extracurricular)
- Impute missing values with `MostFrequent`.
- Encode using `OneHotEncoder(drop='first')` to prevent multicollinearity.

**Numerical Features:** (e.g., Age, Attendance, Marks, Study Hours, Backlogs)
- Impute missing values with `Median`.
- Scale using `StandardScaler` (critical for Logistic Regression/SVM, less important for Tree-based models).

### Step 2.3: Model Training
- Split data: 80% Training, 20% Testing.
- Initialize `RandomForestClassifier` (primary candidate) or `LogisticRegression`.
- Fit the pipeline: `pipeline.fit(X_train, y_train)`

### Step 2.4: Model Evaluation
- Run predictions on `X_test`.
- Calculate Accuracy, Precision, Recall, F1-Score.
- Plot Confusion Matrix to understand false positives (labeling low risk as high risk) vs false negatives (missing high-risk students).

### Step 2.5: Model Persistence
- Save the entire trained pipeline using `joblib.dump(pipeline, 'models/risk_model.joblib')`.
- This ensures the UI application can simply call `pipeline.predict(new_data)` without re-writing the scaling/encoding logic.

## 3. Data Leakage Prevention
Target columns (performance_category and isk_level) and identifiers (student_id, 
ame) are explicitly excluded from the NUMERICAL_FEATURES and CATEGORICAL_FEATURES arrays. The preprocessing pipeline strictly fits on training data only.

## 4. Preprocessing
- **Numerical**: Scaled using StandardScaler.
- **Categorical**: One-hot encoded using OneHotEncoder(handle_unknown='ignore').

## 5. Model Selection & Results
Three models (Logistic Regression, Decision Tree, Random Forest) are trained for both targets. Based on actual Phase 3 evaluation:
- **Performance Model**: Logistic Regression selected (Accuracy: ~94%)
- **Risk Model**: Logistic Regression selected (Accuracy: ~97%)

*For detailed results, see docs/ml_results.md.*

## 6. Model Persistence
The entire pipeline (preprocessing + classifier) is saved to avoid skew during inference using joblib. Artifacts:
- models/performance_model.joblib`n- models/risk_model.joblib`n
## 7. Prediction Workflow
The GUI will invoke services/prediction_service.py, which isolates ML inference from the application layer. The service records historical predictions in the SQLite database.