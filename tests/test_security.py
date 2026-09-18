import pytest
from utils.security import hash_password, verify_password

def test_password_hashing():
    password = "SecurePassword123!"
    hashed = hash_password(password)
    
    assert hashed != password
    assert ":" in hashed  # Should contain salt:hash
    
    salt, hash_part = hashed.split(":")
    assert len(salt) > 0
    assert len(hash_part) > 0

def test_password_verification():
    password = "MySecretPassword"
    hashed = hash_password(password)
    
    # Correct verification
    assert verify_password(hashed, password) is True
    
    # Incorrect verification
    assert verify_password(hashed, "WrongPassword") is False
    assert verify_password(hashed, "mysecretpassword") is False
    
def test_invalid_hash_format():
    assert verify_password("invalid_format_string", "password") is False
