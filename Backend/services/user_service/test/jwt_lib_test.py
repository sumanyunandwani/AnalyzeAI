# Test suite for JWTLibrary class
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone
from jose import jwt
import pytest
from core.jwt_lib import JWTLibrary

@pytest.fixture
def mock_generate_id():
    """
    Mock GenerateId class to return a

    Returns:
        MagicMock: Mock object simulating GenerateId behavior.
    """
    mock_obj = MagicMock()
    mock_obj.generate_user_id.return_value = "mock_user_id"
    return mock_obj

@pytest.fixture
def jwt_lib(mock_generate_id):
    """
    Fixture to create an instance of JWTLibrary with a mocked GenerateId.

    Args:
        mock_generate_id (MagicMock): Mocked GenerateId instance.

    Returns:
        JWTLibrary: An instance of JWTLibrary with mocked dependencies.
    """
    with patch("core.jwt_lib.GenerateId", return_value=mock_generate_id):
        return JWTLibrary(logger=MagicMock())

@pytest.mark.asyncio
async def test_create_and_decode_jwt(jwt_lib: JWTLibrary):
    """
    Test creating and decoding a JWT token.

    Args:
        jwt_lib (JWTLibrary): Instance of JWTLibrary to test.
    """
    payload = {"user_id": 123}
    token = await jwt_lib.create_jwt(payload)
    decoded = await jwt_lib.decode_jwt(token)
    assert decoded["user_id"] == 123
    assert "exp" in decoded

@pytest.mark.asyncio
async def test_decode_jwt_none(jwt_lib: JWTLibrary):
    """
    Test decoding a None token.

    Args:
        jwt_lib (JWTLibrary): Instance of JWTLibrary to test.
    """
    assert await jwt_lib.decode_jwt(None) is None

@pytest.mark.asyncio
async def test_decode_jwt_invalid(jwt_lib: JWTLibrary):
    """
    Test decoding an invalid JWT token.

    Args:
        jwt_lib (JWTLibrary): Instance of JWTLibrary to test.
    """
    assert await jwt_lib.decode_jwt("invalid_token") is None

@pytest.mark.asyncio
async def test_decode_jwt_expired(jwt_lib: JWTLibrary):
    """
    Test decoding an expired JWT token.

    Args:
        jwt_lib (JWTLibrary): Instance of JWTLibrary to test.
    """
    expired_payload = {
        "user_id": 123,
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
    }
    token = jwt.encode(
        expired_payload, jwt_lib._secret_key, algorithm=jwt_lib._algorithm)
    assert await jwt_lib.decode_jwt(token) is None

@pytest.mark.asyncio
async def test_generate_jwt_token_schema(jwt_lib: JWTLibrary, mock_generate_id):
    """
    Test generating JWT token schema.

    Args:
        jwt_lib (JWTLibrary): Instance of JWTLibrary to test.
        mock_generate_id (MagicMock): Mocked GenerateId instance.
    """
    token = {"access": "abc"}
    user = {"name": "John Doe", "email": "john@example.com"}
    schema = await jwt_lib.generate_jwt_token_schema(token, user, "Google")
    assert schema["name"] == "John Doe"
    assert schema["email"] == "john@example.com"
    assert schema["user_id"] == "mock_user_id"
    assert schema["oauth_tag"] == "Google"

@pytest.mark.asyncio
async def test_generate_jwt_from_token(jwt_lib: JWTLibrary):
    """
    Test generating JWT from token, user, and tag.

    Args:
        jwt_lib (JWTLibrary): Instance of JWTLibrary to test.
    """
    token = {"access": "abc"}
    user = {"name": "John Doe", "email": "john@example.com"}
    jwt_token = await jwt_lib.generate_jwt_from_token(token, user, "Github")
    decoded = await jwt_lib.decode_jwt(jwt_token)
    assert decoded.get("oauth_tag") == "Github"
    assert decoded.get("name") == "John Doe"
    assert decoded.get("email") == "john@example.com"
