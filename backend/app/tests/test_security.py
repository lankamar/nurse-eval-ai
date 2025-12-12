import pytest
from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, verify_token,
    generate_totp_secret, verify_totp
)


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_verify_token():
    """Test JWT token creation and verification."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "testuser"


def test_verify_invalid_token():
    """Test verification of invalid token."""
    invalid_token = "invalid.token.here"
    payload = verify_token(invalid_token)
    assert payload is None


def test_generate_totp_secret():
    """Test TOTP secret generation."""
    secret = generate_totp_secret()
    assert secret is not None
    assert isinstance(secret, str)
    assert len(secret) == 32  # Base32 encoded secret


def test_totp_verification():
    """Test TOTP token verification (basic test)."""
    import pyotp
    
    secret = generate_totp_secret()
    totp = pyotp.TOTP(secret)
    token = totp.now()
    
    assert verify_totp(secret, token) is True
    assert verify_totp(secret, "000000") is False
