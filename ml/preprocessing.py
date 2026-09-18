import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

NUMERICAL_FEATURES = [
    'age', 'semester', 'attendance', 'internal_marks', 'assignment_marks',
    'previous_percentage', 'study_hours', 'assignment_completion',
    'participation', 'backlogs'
]

CATEGORICAL_FEATURES = [
    'gender', 'department', 'extracurricular'
]

TARGET_COLUMNS = ['performance_category', 'risk_level']
EXCLUDE_COLUMNS = ['student_id', 'name']

def get_preprocessor() -> ColumnTransformer:
    """
    Returns a scikit-learn ColumnTransformer that scales numerical features
    and one-hot encodes categorical features.
    """
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERICAL_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ]
    )

    return preprocessor

def get_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    """
    Extracts the output feature names from the fitted preprocessor.
    """
    feature_names = []
    
    # Numerical features pass through the scaler but keep their names
    feature_names.extend(NUMERICAL_FEATURES)
    
    # Categorical features are expanded by OneHotEncoder
    if hasattr(preprocessor.named_transformers_['cat'].named_steps['onehot'], 'get_feature_names_out'):
        cat_features = preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(CATEGORICAL_FEATURES)
        feature_names.extend(cat_features)
    
    return feature_names
