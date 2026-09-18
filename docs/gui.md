# GUI & Application Interface

## Overview
The Desktop application is built using **CustomTkinter** for a modern, dark/light mode compatible interface, and **Tkinter** standard libraries where necessary (e.g., `ttk.Treeview` for data grids).

The application architecture enforces strict separation of concerns. The GUI strictly handles presentation and user interaction, delegating all database queries, ML predictions, and business logic to the underlying Service Layer.

## Architecture
- **Entry Point**: `app.py` initializes the SQLite database and launches the root `CTk` window.
- **Routing**: `app.py` acts as a view controller, swapping frames within the main content area (e.g., `dashboard`, `students`, `profile`, `analytics`) without launching multiple root windows.
- **State Management**: `ui/session.py` implements a Singleton `AppSession` to manage the currently logged-in user, enforcing role-based rendering.
- **Theme configuration**: Centralized in `ui/theme.py` to ensure consistent colors, typography, and semantic feedback indicators (Success/Warning/Danger).

## Main Screens
1. **Login** (`ui/login.py`): Authenticates users against the SQLite DB using `PBKDF2 HMAC`.
2. **Dashboard** (`ui/dashboard.py`):
   - **Admin**: Displays aggregate statistics (Total Students, Risk distributions).
   - **Student**: Displays personal academic metrics and current prediction summary.
3. **Student Management** (`ui/student_view.py`): Provides a scrollable, filterable `Treeview` for Admins to search and manage the student dataset.
4. **Prediction / Profile View** (`ui/prediction_view.py`): 
   - Displays student details.
   - Retrieves historical predictions or generates new ones.
   - Renders ML predictions, Risk Score, colored Risk Badges, and prioritized Recommendations.
5. **Analytics** (`ui/analytics_view.py`): Renders dynamically generated Matplotlib `FigureCanvasTkAgg` charts representing Risk and Performance distributions across the entire institutional dataset.

## Role Permissions
- **Admin**: Has global access to the sidebar navigation. Can view the aggregate Dashboard, manage the Student list, run Predictions on any student, and view global Analytics.
- **Student**: Restricted navigation. Can only access their personal Dashboard and Profile/Prediction view. Attempting to navigate outside these boundaries is blocked by the Sidebar logic and `session.is_admin()` checks.

## Prediction Workflow
1. Admin opens the Student list and selects a student.
2. The Profile View loads existing historical data.
3. Admin clicks **Analyze Student**.
4. The GUI calls `PredictionService.run_prediction_for_student(student_id)`.
5. The Service Layer fetches data, runs the ML `predict()`, calculates Risk Scores, generates Recommendations, and persists the results.
6. The GUI refreshes the view using the updated database records, rendering new Badges and recommendation text.

## Demo Flow
To manually verify the application:
```bash
python app.py
```
1. Login as `admin` (Password: `Admin@123`).
2. Explore the Dashboard.
3. Navigate to **Students** and search for `STU0001`.
4. Click **View Profile**.
5. Click **Analyze Student** to trigger the ML & Risk engine.
6. Navigate to **Analytics** to view Matplotlib charts.
7. Click **Logout**.
8. Login as `STU0001` (Password: `Student@123`) to verify restricted student access.
