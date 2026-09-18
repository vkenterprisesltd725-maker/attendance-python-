# Dataset Information

**IMPORTANT: The dataset contained in this directory is strictly SYNTHETIC. It was generated programmatically for development, testing, and demonstration purposes. It does not represent any real educational institution or students.**

## `sample_students.csv`
This file contains 1,000 synthetic records of student academic and demographic data. 

### Data Dictionary

| Column | Type | Description | Range / Values |
|---|---|---|---|
| `student_id` | String | Unique student identifier | STU0001 - STU1000 |
| `name` | String | Synthetic student name | e.g. "Aarav Sharma" |
| `age` | Integer | Student age | 17 - 24 |
| `gender` | String | Student gender | Male, Female, Other |
| `department` | String | Academic department | CSE, IT, ECE, EEE, Mechanical, Civil |
| `semester` | Integer | Current semester of enrollment | 1 - 8 |
| `attendance` | Float | Class attendance percentage | 30.0 - 100.0 |
| `internal_marks` | Float | Continuous internal assessment score | 20.0 - 100.0 |
| `assignment_marks` | Float | Assignment/Project marks | 20.0 - 100.0 |
| `previous_percentage` | Float | Academic percentage from the previous semester | 30.0 - 100.0 |
| `study_hours` | Float | Self-reported daily study hours | 0.0 - 10.0 |
| `assignment_completion`| Float | Percentage of assignments submitted on time | 10.0 - 100.0 |
| `participation` | Float | Metric representing in-class engagement | 0.0 - 100.0 |
| `backlogs` | Integer | Number of uncleared previous subjects | 0 - 5 |
| `extracurricular` | String | Participates in extracurricular activities? | Yes, No |
| `performance_category` | String | TARGET: Binned academic performance score | Needs Improvement, Average, Good, Excellent |
| `risk_level` | String | TARGET: Academic risk classification | Low, Medium, High |

### Target Generation Methodology
The `performance_category` and `risk_level` targets are derived from an internal `calculated_score` (which acts as a composite academic index). The score weights are:
- Attendance: 15%
- Internal Marks: 25%
- Assignment Marks: 15%
- Previous Percentage: 20%
- Study Hours: 10%
- Assignment Completion: 10%
- Participation: 5%
*(A flat penalty of -5 points per backlog is subtracted from the total.)*

**Performance Category Thresholds:**
- >= 80: Excellent
- >= 65: Good
- >= 50: Average
- < 50: Needs Improvement

**Risk Level Thresholds:**
- >= 65: Low Risk
- >= 50: Medium Risk
- < 50: High Risk
