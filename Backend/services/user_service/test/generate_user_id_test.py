# Test suite for GenerateId class
import hashlib
from Backend.services.bdoc_generator_sql_service.core.generate_id import GenerateId


def test_generate_user_id_with_email():
    """
    Test generating a user ID with both name and email.
    """
    generator = GenerateId()
    name = "Alice"
    email = "alice@example.com"
    expected = hashlib.sha256(
        f"{name.lower().strip()}|{email.lower().strip()}".encode("utf-8")).hexdigest()
    result = generator.generate_user_id(name, email)
    assert result == expected


def test_generate_user_id_without_email():
    """
    Test generating a user ID with only name, using default email.
    """
    generator = GenerateId()
    name = "Bob"
    email = None
    default_email = "not_found@not_found.com"
    expected = hashlib.sha256(f"{name.lower().strip()}|{default_email}".encode("utf-8")).hexdigest()
    result = generator.generate_user_id(name, email)
    assert result == expected


def test_generate_request_id():
    """
    Test generating a request ID based on SQL script and business name.
    """
    generator = GenerateId()
    sql_script = "SELECT * FROM users"
    business_name = "Retail"
    expected = hashlib.sha256(
        f"{sql_script.lower().strip()}|{business_name.lower().strip()}".encode("utf-8")).hexdigest()
    result = generator.generate_request_id(sql_script, business_name)
    assert result == expected
