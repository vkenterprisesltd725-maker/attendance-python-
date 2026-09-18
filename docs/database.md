# Database Design

## Database Technology
- **Engine:** SQLite (`sqlite3` built into Python)
- **Database File:** `database/student_performance.db`

## ER Diagram (Textual)

```text
USERS
  │ (1)
  │ 
  │ student_id (optional, nullable)
  │ 
  ▼ (0..1)
STUDENTS
  │ (1)
  ├──────────────► (0..N) PREDICTIONS
  │
  └──────────────► (0..N) RECOMMENDATIONS
```

## Schema Definitions

### `users`
Stores login credentials and roles.
- `id` (INTEGER, PRIMARY KEY)
- `username` (TEXT, UNIQUE, NOT NULL)
- `password_hash` (TEXT, NOT NULL)
- `role` (TEXT, NOT NULL) — 'admin' or 'student'
- `student_id` (TEXT, UNIQUE) — Nullable. If role is student, links to `students.student_id`.
- `created_at` (TIMESTAMP)

### `students`
Stores academic and demographic data.
- `student_id` (TEXT, PRIMARY KEY)
- `name` (TEXT, NOT NULL)
- `age` (INTEGER)
- `gender` (TEXT)
- `department` (TEXT)
- `semester` (INTEGER)
- `attendance` (REAL)
- `internal_marks` (REAL)
- `assignment_marks` (REAL)
- `previous_percentage` (REAL)
- `study_hours` (REAL)
- `assignment_completion` (REAL)
- `participation` (REAL)
- `backlogs` (INTEGER)
- `extracurricular` (TEXT)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### `predictions`
Stores historical ML inference results.
- `prediction_id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `student_id` (TEXT, FOREIGN KEY references `students.student_id`)
- `predicted_category` (TEXT) — e.g., 'Good', 'Needs Improvement'
- `risk_level` (TEXT) — e.g., 'Low', 'High'
- `risk_score` (REAL)
- `model_name` (TEXT)
- `prediction_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### `recommendations`
Stores personalized advice generated for a student.
- `recommendation_id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `student_id` (TEXT, FOREIGN KEY references `students.student_id`)
- `recommendation` (TEXT)
- `priority` (TEXT) — 'High', 'Medium', 'Low'
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

## Foreign Keys & Relationships
- A `User` (if a student) maps 1:1 to a `Student`.
- A `Student` maps 1:N to `Predictions` (tracking performance over time).
- A `Student` maps 1:N to `Recommendations`.
- Deleting a `Student` will CASCADE delete their `Predictions` and `Recommendations`.
