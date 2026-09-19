import pandas as pd
import numpy as np
import json
import random
import sys
from pathlib import Path

def generate_dataset(num_records=10, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    # Base characteristics
    student_ids = [f"STU{str(i).zfill(4)}" for i in range(1, num_records + 1)]
    
    # Names (synthetic)
    first_names = ["Aarav", "Vihaan", "Aditya", "Arjun", "Sai", "Riya", "Aanya", "Diya", "Ananya", "Ishita", "Rahul", "Karan", "Sneha", "Neha", "Priya", "Vikram", "Rohan", "Meera", "Kavya", "Arun"]
    last_names = ["Sharma", "Patel", "Kumar", "Singh", "Gupta", "Verma", "Reddy", "Rao", "Desai", "Jain", "Bose", "Das", "Roy", "Chowdhury", "Menon", "Pillai", "Nair", "Iyer"]
    names = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(num_records)]
    
    ages = np.random.randint(17, 25, size=num_records)
    genders = np.random.choice(["Male", "Female", "Other"], size=num_records, p=[0.55, 0.43, 0.02])
    departments = np.random.choice(["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"], size=num_records, p=[0.3, 0.2, 0.15, 0.15, 0.1, 0.1])
    semesters = np.random.randint(1, 9, size=num_records)

    # Generate latent academic ability to create correlated features
    # Normal distribution centered around 0.65
    base_ability = np.clip(np.random.normal(0.65, 0.15, size=num_records), 0.2, 1.0)
    
    # Correlated academic features with noise
    attendance = np.clip(base_ability * 100 + np.random.normal(0, 10, num_records), 30, 100)
    internal_marks = np.clip(base_ability * 100 + np.random.normal(0, 8, num_records), 20, 100)
    assignment_marks = np.clip(base_ability * 100 + np.random.normal(0, 8, num_records), 20, 100)
    previous_percentage = np.clip(base_ability * 100 + np.random.normal(0, 7, num_records), 30, 100)
    
    study_hours = np.clip(base_ability * 8 + np.random.normal(0, 1.5, num_records), 0, 10)
    assignment_completion = np.clip(base_ability * 100 + np.random.normal(0, 12, num_records), 10, 100)
    participation = np.clip(base_ability * 100 + np.random.normal(0, 15, num_records), 0, 100)
    
    # Backlogs (inverse to base ability)
    backlogs_prob = 1.0 - base_ability
    backlogs = np.clip(np.random.poisson(backlogs_prob * 3), 0, 5)
    
    extracurricular = np.random.choice(["Yes", "No"], size=num_records, p=[0.4, 0.6])

    # Construct DataFrame
    df = pd.DataFrame({
        "student_id": student_ids,
        "name": names,
        "age": ages,
        "gender": genders,
        "department": departments,
        "semester": semesters,
        "attendance": np.round(attendance, 1),
        "internal_marks": np.round(internal_marks, 1),
        "assignment_marks": np.round(assignment_marks, 1),
        "previous_percentage": np.round(previous_percentage, 1),
        "study_hours": np.round(study_hours, 1),
        "assignment_completion": np.round(assignment_completion, 1),
        "participation": np.round(participation, 1),
        "backlogs": backlogs,
        "extracurricular": extracurricular
    })

    # Calculate Target Score
    # Attendance: 15%, Internal: 25%, Assignment: 15%, Prev: 20%, Study: 10%, Comp: 10%, Part: 5%
    df['calculated_score'] = (
        df['attendance'] * 0.15 +
        df['internal_marks'] * 0.25 +
        df['assignment_marks'] * 0.15 +
        df['previous_percentage'] * 0.20 +
        (df['study_hours'] / 10 * 100) * 0.10 +
        df['assignment_completion'] * 0.10 +
        df['participation'] * 0.05
    )
    
    # Apply backlog penalty (e.g., -5 points per backlog)
    df['calculated_score'] = df['calculated_score'] - (df['backlogs'] * 5)
    df['calculated_score'] = np.clip(df['calculated_score'], 0, 100)

    # Generate Targets based on the calculated score
    def categorize_performance(score):
        if score >= 80: return "Excellent"
        elif score >= 65: return "Good"
        elif score >= 50: return "Average"
        else: return "Needs Improvement"

    def categorize_risk(score):
        if score >= 65: return "Low"
        elif score >= 50: return "Medium"
        else: return "High"

    df['performance_category'] = df['calculated_score'].apply(categorize_performance)
    df['risk_level'] = df['calculated_score'].apply(categorize_risk)
    
    # Drop intermediate score column
    df.drop(columns=['calculated_score'], inplace=True)

    # Validations
    try:
        assert len(df) == num_records, f"Must have exactly {num_records} rows."
        assert df['student_id'].nunique() == num_records, "Student IDs must be unique."
        assert not df.isnull().values.any(), "Missing values found."
        
        numeric_cols = ['age', 'semester', 'attendance', 'internal_marks', 'assignment_marks', 
                        'previous_percentage', 'study_hours', 'assignment_completion', 'participation', 'backlogs']
        for col in numeric_cols:
            assert (df[col] >= 0).all(), f"Negative values found in {col}."
            
        # Class distribution check (ensure no class is 0%)
        perf_dist = df['performance_category'].value_counts(normalize=True)
        risk_dist = df['risk_level'].value_counts(normalize=True)
        
        for p in ['Excellent', 'Good', 'Average', 'Needs Improvement']:
            if p not in perf_dist or perf_dist[p] < 0.05:
                print(f"Warning: Poor distribution for performance category {p} ({perf_dist.get(p, 0):.2f})")
                
    except AssertionError as e:
        print(f"Validation failed: {e}")
        sys.exit(1)

    # Save outputs
    output_dir = Path(__file__).resolve().parent
    csv_path = output_dir / "sample_students.csv"
    df.to_csv(csv_path, index=False)

    # Summary
    summary = {
        "num_records": len(df),
        "num_features": len(df.columns) - 2, # ex target
        "numeric_columns": numeric_cols,
        "categorical_columns": ['student_id', 'name', 'gender', 'department', 'extracurricular'],
        "performance_distribution": df['performance_category'].value_counts().to_dict(),
        "risk_distribution": df['risk_level'].value_counts().to_dict(),
        "random_seed": seed
    }
    
    json_path = output_dir / "dataset_summary.json"
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=4)
        
    print(f"Dataset generated successfully at {csv_path}")
    print(f"Summary saved to {json_path}")
    
    # Print quality check
    print("\\n--- Quality Check ---")
    print("Total Records:", len(df))
    print("Missing Values:", df.isnull().sum().sum())
    print("Duplicate IDs:", df.duplicated(subset=['student_id']).sum())
    print("Performance Distribution:\\n", df['performance_category'].value_counts())
    print("Risk Distribution:\\n", df['risk_level'].value_counts())

if __name__ == "__main__":
    generate_dataset()
