import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.config import DATA_DIR, MODELS_DIR
from ml.preprocessing import get_preprocessor, NUMERICAL_FEATURES, CATEGORICAL_FEATURES, get_feature_names

def load_data(filepath: Path) -> pd.DataFrame:
    '''Loads and validates the dataset.'''
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    df = pd.read_csv(filepath)
    
    # Validation
    required_cols = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + ['performance_category', 'risk_level']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")
        
    if df.isnull().values.any():
        raise ValueError("Dataset contains missing values.")
        
    return df

def train_and_evaluate_models(X_train, y_train, X_test, y_test, target_name):
    '''Trains 3 models and returns their evaluation metrics and pipelines.'''
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        'Decision Tree': DecisionTreeClassifier(max_depth=10, min_samples_split=5, random_state=42, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
    }
    
    results = {}
    pipelines = {}
    
    for name, classifier in models.items():
        print(f"Training {name} for {target_name}...")
        pipeline = Pipeline(steps=[
            ('preprocessor', get_preprocessor()),
            ('classifier', classifier)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = {
            'accuracy': float(acc),
            'precision': float(prec),
            'recall': float(rec),
            'f1': float(f1)
        }
        pipelines[name] = pipeline
        
        # Save Confusion Matrix plot
        save_confusion_matrix(cm, pipeline.classes_, name, target_name)
        
    return results, pipelines

def save_confusion_matrix(cm, classes, model_name, target_name):
    '''Saves confusion matrix as an image.'''
    eval_dir = MODELS_DIR / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title(f'Confusion Matrix: {model_name} ({target_name})')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    
    safe_model_name = model_name.replace(' ', '_').lower()
    plt.savefig(eval_dir / f"{target_name}_{safe_model_name}_cm.png")
    plt.close()

def select_best_model(results, pipelines, target_name):
    '''Selects the best model based on F1-score.'''
    best_name = max(results.keys(), key=lambda k: results[k]['f1'])
    print(f"Selected {best_name} for {target_name} (F1: {results[best_name]['f1']:.4f})")
    return best_name, pipelines[best_name], results[best_name]

def extract_feature_importance(pipeline, target_name):
    '''Extracts and saves feature importance if applicable.'''
    classifier = pipeline.named_steps['classifier']
    preprocessor = pipeline.named_steps['preprocessor']
    
    if hasattr(classifier, 'feature_importances_'):
        importances = classifier.feature_importances_
        feature_names = get_feature_names(preprocessor)
        
        importance_dict = {name: float(imp) for name, imp in zip(feature_names, importances)}
        importance_dict = dict(sorted(importance_dict.items(), key=lambda item: item[1], reverse=True))
        
        with open(MODELS_DIR / f"{target_name}_feature_importance.json", 'w') as f:
            json.dump(importance_dict, f, indent=4)
            
        # Plot top 10
        top_k = dict(list(importance_dict.items())[:10])
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(top_k.values()), y=list(top_k.keys()), palette='viridis')
        plt.title(f'Top 10 Feature Importances: {target_name}')
        plt.tight_layout()
        plt.savefig(MODELS_DIR / "evaluation" / f"{target_name}_feature_importance.png")
        plt.close()

def main():
    print("Starting ML pipeline execution...")
    data_path = DATA_DIR / "sample_students.csv"
    
    df = load_data(data_path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Features (X) exclude targets and IDs
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    
    targets = ['performance_category', 'risk_level']
    all_results = {}
    metadata = {
        'training_timestamp': datetime.now().isoformat(),
        'train_size': 0.8,
        'test_size': 0.2,
        'random_seed': 42,
        'features': {
            'numerical': NUMERICAL_FEATURES,
            'categorical': CATEGORICAL_FEATURES
        },
        'models': {}
    }
    
    for target in targets:
        print(f"\\n--- Training for {target} ---")
        y = df[target]
        
        # Train/Test Split (Stratified to handle class imbalance safely)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"Train set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")
        
        results, pipelines = train_and_evaluate_models(X_train, y_train, X_test, y_test, target)
        all_results[target] = results
        
        best_name, best_pipeline, best_metrics = select_best_model(results, pipelines, target)
        
        # Save Model
        model_filename = f"{target.split('_')[0]}_model.joblib"
        joblib.dump(best_pipeline, MODELS_DIR / model_filename)
        
        # Extract feature importance
        extract_feature_importance(best_pipeline, target)
        
        metadata['models'][target] = {
            'selected_model': best_name,
            'metrics': best_metrics,
            'artifact': model_filename,
            'classes': best_pipeline.classes_.tolist()
        }
    
    # Save Model Comparison
    with open(MODELS_DIR / "model_comparison.json", 'w') as f:
        json.dump(all_results, f, indent=4)
        
    # Save Metadata
    with open(MODELS_DIR / "model_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("\\nML pipeline executed successfully. Artifacts saved in models/")

if __name__ == '__main__':
    main()
