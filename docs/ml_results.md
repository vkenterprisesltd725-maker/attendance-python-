# Machine Learning Results

## Dataset
- **Records:** 1000 synthetic records
- **Split:** 80% Training (800 records), 20% Testing (200 records)
- **Random Seed:** 42 (Stratified splitting)

## Features
**Predictive Features Used:**
- `age`, `semester`, `attendance`, `internal_marks`, `assignment_marks`, `previous_percentage`, `study_hours`, `assignment_completion`, `participation`, `backlogs`
- `gender`, `department`, `extracurricular`

*(Target variables and unique identifiers like `student_id` were strictly excluded to prevent data leakage).*

## Performance Prediction (Target: `performance_category`)

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
|---|---|---|---|---|
| **Logistic Regression** | **0.940** | **0.946** | **0.940** | **0.940** |
| Random Forest | 0.860 | 0.863 | 0.860 | 0.861 |
| Decision Tree | 0.745 | 0.753 | 0.745 | 0.747 |

## Risk Prediction (Target: `risk_level`)

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
|---|---|---|---|---|
| **Logistic Regression** | **0.970** | **0.970** | **0.970** | **0.970** |
| Random Forest | 0.855 | 0.876 | 0.855 | 0.859 |
| Decision Tree | 0.835 | 0.836 | 0.835 | 0.835 |

## Confusion Matrices
Saved under `models/evaluation/`:
- `performance_category_logistic_regression_cm.png`
- `performance_category_random_forest_cm.png`
- `performance_category_decision_tree_cm.png`
- `risk_level_logistic_regression_cm.png`
- `risk_level_random_forest_cm.png`
- `risk_level_decision_tree_cm.png`

## Selected Models
**Logistic Regression** was automatically selected for both tasks because it achieved the highest F1-Score (0.9404 and 0.9701).

**Why did Logistic Regression perform best?**
The synthetic target variables (`performance_category` and `risk_level`) were generated using a weighted linear combination of numerical features (with some injected noise). Because Logistic Regression is a linear model, it perfectly captures this underlying linear relationship. Random Forests and Decision Trees struggled slightly more to map the continuous linear boundaries with limited depth constraints.

## Limitations
1. **Synthetic Dataset**: The model predicts patterns that were synthetically injected. Real-world institutional data will likely be much noisier and have non-linear relationships, where Random Forest might ultimately outperform Logistic Regression.
2. **Feature Limits**: Missing critical socioeconomic or psychological features that often influence real academic risk.
3. **No Guarantees**: Predictions are statistical estimates and should not be used for automated high-stakes academic decisions without human review.

## Disclaimer
**IMPORTANT**: The current dataset is synthetic and therefore model performance should not be interpreted as real-world clinical/educational predictive validity. The high accuracy is reflective of the logical constraints built into the synthetic data generation script.