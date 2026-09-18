# System Architecture

## Overview
The system employs a classic layered architecture (N-Tier) to ensure separation of concerns, testability, and maintainability.

## Layered Architecture Diagram

```text
┌────────────────────────────────────────────────────────┐
│                   Python GUI Layer                     │
│                Tkinter / CustomTkinter                 │
│  (Views: Login, Dashboard, Student, Prediction, etc.)  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                     Service Layer                      │
│   (Business Logic, Data Orchestration, ML Execution)   │
│   StudentService | PredictionService | ReportService   │
└───────────┬───────────────────────────────┬────────────┘
            │                               │
    ┌───────▼────────┐              ┌───────▼────────┐
    │  Data Access   │              │   ML Pipeline  │
    │  (SQLite DB)   │              │ (Scikit-Learn) │
    └───────┬────────┘              └───────┬────────┘
            │                               │
     ┌──────▼──────┐                 ┌──────▼──────┐
     │ Database.db │                 │ Model Files │
     └─────────────┘                 └─────────────┘
```

## Layer Descriptions

### 1. Presentation Layer (Python GUI Layer)
**Technology:** `tkinter` and `customtkinter`
**Responsibility:** Handles all user interactions, capturing input, displaying data, rendering charts (via `matplotlib` embedded in `tkinter`), and routing user actions to the Service Layer. Contains no raw database SQL or direct ML logic.

### 2. Service Layer
**Technology:** Pure Python
**Responsibility:** The core engine of the application. It orchestrates the flow of data.
- `student_service.py`: CRUD operations for students.
- `prediction_service.py`: Interfaces with the ML pipeline to score students.
- `recommendation_service.py`: Maps risk scores/factors to actionable advice.
- `report_service.py`: Uses `reportlab` to generate PDFs.

### 3. Data Access Layer
**Technology:** `sqlite3`
**Responsibility:** Manages all direct database interactions. Executes parameterized SQL statements to read/write records. Handles schema initialization.

### 4. ML Pipeline Layer
**Technology:** `scikit-learn`, `pandas`, `numpy`, `joblib`
**Responsibility:** Defines the model, trains it, evaluates it, and exports it. During runtime, it loads the `.joblib` model artifact to run inferences on new student data.
