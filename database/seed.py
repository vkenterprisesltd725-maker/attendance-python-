import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from database.database import initialize_database, execute_query, fetch_one
from utils.security import hash_password
from config.config import DB_PATH, DATA_DIR
from services.student_service import StudentService

def seed_database():
    print("Initializing Database Schema...")
    initialize_database()

    print("Seeding Users...")
    
    # 1. Admin User
    admin_username = "admin"
    admin_password = "Admin@123"
    
    existing_admin = fetch_one("SELECT * FROM users WHERE username = ?", (admin_username,))
    if not existing_admin:
        execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (admin_username, hash_password(admin_password), 'admin')
        )
        print(f"Created Admin user: {admin_username}")
    else:
        print("Admin user already exists.")

    # 2. Seed Students from Sample Data
    sample_csv = DATA_DIR / "sample_students.csv"
    if sample_csv.exists():
        print(f"Importing sample students from {sample_csv}...")
        success, fails, errors = StudentService.import_from_file(str(sample_csv))
        print(f"Import complete: {success} added, {fails} failed/skipped.")
        if fails > 0 and len(errors) > 0:
            print("Note: First few skip reasons:")
            for e in errors[:5]:
                print(f"  - {e}")
    else:
        print(f"Sample dataset not found at {sample_csv}. Run data/generate_dataset.py first.")


    # 3. Demo Student User
    demo_username = "STU0001"
    demo_password = "Student@123"
    
    existing_student = fetch_one("SELECT * FROM users WHERE username = ?", (demo_username,))
    if not existing_student:
        execute_query(
            "INSERT INTO users (username, password_hash, role, student_id) VALUES (?, ?, ?, ?)",
            (demo_username, hash_password(demo_password), 'student', demo_username)
        )
        print(f"Created Demo Student user: {demo_username}")
    else:
        print("Demo Student user already exists.")

if __name__ == "__main__":
    seed_database()
