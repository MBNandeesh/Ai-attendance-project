from app.core.security import create_access_token, decode_token, hash_password, verify_password


def test_password_hash_roundtrip():
    hashed = hash_password("mypassword123")
    assert hashed != "mypassword123"
    assert verify_password("mypassword123", hashed)
    assert not verify_password("wrongpassword", hashed)


def test_access_token_roundtrip():
    token = create_access_token("42", "teacher")
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert payload["role"] == "teacher"
    assert payload["type"] == "access"


def test_invalid_token_returns_none():
    assert decode_token("not-a-real-token") is None
