import hashlib
import os

def hash_password(password: str) -> str:
    """
    Hashes a password using PBKDF2 HMAC with SHA-256.
    Returns a string containing the salt and hash.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"{salt.hex()}:{pw_hash.hex()}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    Verifies a provided password against the stored salt:hash string.
    """
    try:
        salt_hex, hash_hex = stored_password.split(':')
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        
        pw_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        
        # Use compare_digest to prevent timing attacks
        import hmac
        return hmac.compare_digest(pw_hash, expected_hash)
    except Exception:
        return False
