import os
import sys
import json
import joblib
from pathlib import Path
from sklearn.metrics import classification_report

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.config import MODELS_DIR
from ml.train_model import load_data, DATA_DIR, NUMERICAL_FEATURES, CATEGORICAL_FEATURES
from sklearn.model_selection import train_test_split

def evaluate_saved_model(target_name: str, model_filename: str):
    '''Loads a saved model and evaluates it on the test set.'''
    model_path = MODELS_DIR / model_filename
    if not model_path.exists():
        print(f"Model artifact {model_path} not found.")
        return
        
    print(f"Loading {model_path.name}...")
    pipeline = joblib.load(model_path)
    
    df = load_data(DATA_DIR / "sample_students.csv")
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[target_name]
    
    # We must recreate the exact same split to get the test set
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\\n--- Evaluation Report for {target_name} ---")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

def main():
    metadata_path = MODELS_DIR / "model_metadata.json"
    if not metadata_path.exists():
        print("Model metadata not found. Please run train_model.py first.")
        sys.exit(1)
        
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        
    for target_name, info in metadata['models'].items():
        evaluate_saved_model(target_name, info['artifact'])

if __name__ == '__main__':
    main()
