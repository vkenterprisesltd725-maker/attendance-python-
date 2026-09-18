import pytest
import os
from database.database import initialize_database
from services.data_quality_service import DataQualityService
from ui.session import AppSession

TEST_DB = "test_dq.db"

@pytest.fixture(autouse=True)
def setup_teardown(monkeypatch):
    import database.database as db
    monkeypatch.setattr(db, "DB_PATH", TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    initialize_database(db_path=TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except:
            pass

def test_data_quality_empty():
    stats = DataQualityService.get_quality_summary()
    assert stats['total_records'] == 0
    assert stats['missing_values'] == 0
    assert stats['duplicates'] == 0
    assert stats['valid_records'] == 0

def test_authorization_student_cannot_access_admin():
    session = AppSession()
    session.login("STU0001", "student", "STU0001")
    assert session.is_student()
    assert not session.is_admin()

def test_authorization_admin_access():
    session = AppSession()
    session.login("admin", "admin")
    assert session.is_admin()
    assert not session.is_student()
