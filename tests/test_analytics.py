import pytest
import os
from database.database import initialize_database
from services.analytics_service import AnalyticsService

TEST_DB = "test_analytics.db"

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
        except PermissionError:
            pass

def test_get_overview_stats_empty():
    stats = AnalyticsService.get_overview_stats()
    assert stats['total_students'] == 0
    assert stats['high_risk_count'] == 0

def test_get_risk_distribution_empty():
    data = AnalyticsService.get_risk_distribution()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_performance_distribution_empty():
    data = AnalyticsService.get_performance_distribution()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_attendance_data_empty():
    data = AnalyticsService.get_attendance_data()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_backlog_data_empty():
    data = AnalyticsService.get_backlog_data()
    assert isinstance(data, list)
    assert len(data) == 0
