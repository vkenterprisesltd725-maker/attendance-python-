# Data Quality Report

## Dataset Overview
- **Total Records:** 1000
- **Total Features:** 15 (13 predictive + 2 targets)
- **Random Seed:** 42

## Data Quality Checks
- **Missing Values:** 0
- **Duplicate Student IDs:** 0
- **Negative Values (where invalid):** 0

## Columns & Statistics
### Categorical Columns
- `student_id`: Unique identifier (STU0001 - STU1000)
- `name`: Synthetic Name
- `gender`: Male, Female, Other
- `department`: CSE, IT, ECE, EEE, Mechanical, Civil
- `extracurricular`: Yes, No

### Numerical Variables
The dataset accurately simulates a diverse range of student metrics. Built on a normal distribution for latent academic ability, features such as attendance, marks, and study hours are realistically correlated without being a perfect deterministic line (simulated noise injected).

- **Age**: 17 - 24
- **Semester**: 1 - 8
- **Attendance**: 30% - 100%
- **Internal Marks**: 20 - 100
- **Assignment Marks**: 20 - 100
- **Previous Percentage**: 30% - 100%
- **Study Hours**: 0 - 10 hrs/day
- **Assignment Completion**: 10% - 100%
- **Participation**: 0 - 100
- **Backlogs**: 0 - 5

## Target Distributions

### Performance Category
- **Needs Improvement**: 32.6% (326 students)
- **Average**: 31.0% (310 students)
- **Good**: 24.8% (248 students)
- **Excellent**: 11.6% (116 students)

### Risk Level
- **Low Risk**: 36.4% (364 students)
- **Medium Risk**: 31.0% (310 students)
- **High Risk**: 32.6% (326 students)

## Conclusion
The dataset exhibits a reasonable spread across all categories, ensuring the ML algorithms have a robust, balanced set of instances to learn from. The risk levels and performance categories avoid severe class imbalance.
