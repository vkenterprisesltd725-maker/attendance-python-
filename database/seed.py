import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from database.database import initialize_database, execute_query, fetch_one, fetch_all
from utils.security import hash_password
from config.config import DB_PATH, DATA_DIR
from services.student_service import StudentService

def seed_database():
    # Remove existing database for a clean start
    if DB_PATH.exists():
        os.remove(DB_PATH)
        print("Removed old database for a clean start.")

    print("Initializing Database Schema...")
    initialize_database()

    print("Seeding Users...")
    
    # 1. Admin User
    admin_username = "admin"
    admin_password = "Admin@123"
    
    execute_query(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (admin_username, hash_password(admin_password), 'admin')
    )
    print(f"Created Admin user: {admin_username}")

    # 2. Seed Students from Sample Data
    sample_csv = DATA_DIR / "sample_students.csv"
    if sample_csv.exists():
        print(f"Importing sample students from {sample_csv}...")
        success, fails, errors = StudentService.import_from_file(str(sample_csv))
        print(f"Import complete: {success} added, {fails} failed/skipped.")
    else:
        print(f"Sample dataset not found at {sample_csv}. Run data/generate_dataset.py first.")

    # 3. Create a login for EVERY student imported
    students = fetch_all("SELECT student_id FROM students")
    for s in students:
        sid = s['student_id']
        # Set username and password same as student_id
        execute_query(
            "INSERT INTO users (username, password_hash, role, student_id) VALUES (?, ?, ?, ?)",
            (sid, hash_password(sid), 'student', sid)
        )
    print(f"Created {len(students)} student login accounts (username and password = Student ID).")

if __name__ == "__main__":
    seed_database()
