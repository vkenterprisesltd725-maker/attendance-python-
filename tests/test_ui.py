import pytest
from ui.session import AppSession

def test_session_singleton():
    s1 = AppSession()
    s2 = AppSession()
    assert s1 is s2

def test_session_login():
    s = AppSession()
    s.clear()
    assert not s.is_logged_in()
    
    s.login("admin", "admin")
    assert s.is_logged_in()
    assert s.is_admin()
    assert not s.is_student()
    
def test_session_clear():
    s = AppSession()
    s.login("STU0001", "student", "STU0001")
    assert s.is_logged_in()
    
    s.clear()
    assert not s.is_logged_in()
    assert not s.is_admin()
    assert not s.is_student()

def test_session_roles():
    s = AppSession()
    s.login("STU0001", "student", "STU0001")
    assert s.is_student()
    assert not s.is_admin()
