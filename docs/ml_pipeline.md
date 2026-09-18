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

## 3. Data Flow

```text
Student Dataset -> Validation -> Preprocessing (Impute+Scale/Encode) -> Train/Test Split -> Model Training -> Evaluation -> Model Persistence -> Inference (Prediction)
```
