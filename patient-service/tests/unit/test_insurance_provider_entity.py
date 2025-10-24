"""Unit tests for InsuranceProvider entity"""
import pytest
from datetime import datetime

from domain.entities.insurance_provider import InsuranceProvider


def test_create_insurance_provider_with_valid_data():
    """Test creating an insurance provider with valid data"""
    provider = InsuranceProvider.create(
        name="HealthCare Plus",
        code="HCP",
        phone="1234567890",
        email="contact@healthcare.com",
        website="https://www.healthcare.com",
        address="123 Health St, Medical City"
    )

    assert provider.name == "HealthCare Plus"
    assert provider.code == "HCP"
    assert provider.phone == "1234567890"
    assert provider.email == "contact@healthcare.com"
    assert provider.website == "https://www.healthcare.com"
    assert provider.address == "123 Health St, Medical City"
    assert provider.is_active is True
    assert provider.id is not None
    assert isinstance(provider.created_at, datetime)
    assert isinstance(provider.updated_at, datetime)


def test_create_insurance_provider_with_minimal_data():
    """Test creating provider with only required fields"""
    provider = InsuranceProvider.create(
        name="Simple Insurance",
        code="SIM"
    )

    assert provider.name == "Simple Insurance"
    assert provider.code == "SIM"
    assert provider.phone is None
    assert provider.email is None
    assert provider.website is None
    assert provider.address is None
    assert provider.is_active is True


def test_create_insurance_provider_code_uppercase():
    """Test that provider code is converted to uppercase"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="test123"
    )

    assert provider.code == "TEST123"


def test_create_insurance_provider_email_lowercase():
    """Test that email is converted to lowercase"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST",
        email="CONTACT@TEST.COM"
    )

    assert provider.email == "contact@test.com"


def test_create_insurance_provider_with_empty_name():
    """Test creating provider with empty name fails"""
    with pytest.raises(ValueError, match="Provider name cannot be empty"):
        InsuranceProvider.create(
            name="",
            code="TEST"
        )


def test_create_insurance_provider_with_long_name():
    """Test creating provider with name too long fails"""
    with pytest.raises(ValueError, match="Provider name must not exceed 100 characters"):
        InsuranceProvider.create(
            name="A" * 101,
            code="TEST"
        )


def test_create_insurance_provider_with_empty_code():
    """Test creating provider with empty code fails"""
    with pytest.raises(ValueError, match="Provider code cannot be empty"):
        InsuranceProvider.create(
            name="Test Insurance",
            code=""
        )


def test_create_insurance_provider_with_long_code():
    """Test creating provider with code too long fails"""
    with pytest.raises(ValueError, match="Provider code must not exceed 20 characters"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="A" * 21
        )


def test_create_insurance_provider_with_invalid_code():
    """Test creating provider with non-alphanumeric code fails"""
    with pytest.raises(ValueError, match="Provider code must be alphanumeric"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="TEST@#$"
        )


def test_create_insurance_provider_with_code_with_dash():
    """Test creating provider with code containing dash (allowed)"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST-123"
    )

    assert provider.code == "TEST-123"


def test_create_insurance_provider_with_code_with_underscore():
    """Test creating provider with code containing underscore (allowed)"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST_123"
    )

    assert provider.code == "TEST_123"


def test_create_insurance_provider_with_invalid_phone():
    """Test creating provider with invalid phone fails"""
    with pytest.raises(ValueError, match="Phone must contain only digits"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="TEST",
            phone="123-456-7890"
        )


def test_create_insurance_provider_with_phone_too_short():
    """Test creating provider with phone too short fails"""
    with pytest.raises(ValueError, match="Phone must be between 7 and 15 digits"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="TEST",
            phone="123456"
        )


def test_create_insurance_provider_with_phone_too_long():
    """Test creating provider with phone too long fails"""
    with pytest.raises(ValueError, match="Phone must be between 7 and 15 digits"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="TEST",
            phone="1234567890123456"
        )


def test_create_insurance_provider_with_invalid_email():
    """Test creating provider with invalid email fails"""
    with pytest.raises(ValueError, match="Invalid email format"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="TEST",
            email="invalid-email"
        )


def test_create_insurance_provider_with_long_website():
    """Test creating provider with website too long fails"""
    with pytest.raises(ValueError, match="Website URL must not exceed 200 characters"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="TEST",
            website="https://" + "a" * 200 + ".com"
        )


def test_create_insurance_provider_with_long_address():
    """Test creating provider with address too long fails"""
    with pytest.raises(ValueError, match="Address must not exceed 200 characters"):
        InsuranceProvider.create(
            name="Test Insurance",
            code="TEST",
            address="A" * 201
        )


def test_update_insurance_provider_name():
    """Test updating provider name"""
    import time
    provider = InsuranceProvider.create(
        name="Original Name",
        code="TEST"
    )

    original_updated_at = provider.updated_at
    time.sleep(0.01)  # Small delay to ensure different timestamp

    provider.update_info(name="Updated Name")

    assert provider.name == "Updated Name"
    assert provider.updated_at >= original_updated_at


def test_update_insurance_provider_phone():
    """Test updating provider phone"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST",
        phone="1234567890"
    )

    provider.update_info(phone="9876543210")

    assert provider.phone == "9876543210"


def test_update_insurance_provider_email():
    """Test updating provider email"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST",
        email="old@test.com"
    )

    provider.update_info(email="NEW@TEST.COM")

    assert provider.email == "new@test.com"  # Should be lowercase


def test_update_insurance_provider_website():
    """Test updating provider website"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST",
        website="https://old.com"
    )

    provider.update_info(website="https://new.com")

    assert provider.website == "https://new.com"


def test_update_insurance_provider_address():
    """Test updating provider address"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST",
        address="Old Address"
    )

    provider.update_info(address="New Address")

    assert provider.address == "New Address"


def test_update_insurance_provider_multiple_fields():
    """Test updating multiple provider fields at once"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST"
    )

    provider.update_info(
        name="Updated Insurance",
        phone="1234567890",
        email="contact@updated.com"
    )

    assert provider.name == "Updated Insurance"
    assert provider.phone == "1234567890"
    assert provider.email == "contact@updated.com"


def test_update_insurance_provider_clear_optional_fields():
    """Test clearing optional fields by setting to None"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST",
        phone="1234567890",
        email="contact@test.com"
    )

    provider.update_info(phone="", email="")

    assert provider.phone == ""
    assert provider.email is None


def test_update_insurance_provider_with_invalid_name():
    """Test updating provider with invalid name fails"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST"
    )

    with pytest.raises(ValueError, match="Provider name must not exceed 100 characters"):
        provider.update_info(name="A" * 101)


def test_update_insurance_provider_with_invalid_phone():
    """Test updating provider with invalid phone fails"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST"
    )

    with pytest.raises(ValueError, match="Phone must be between 7 and 15 digits"):
        provider.update_info(phone="123")


def test_update_insurance_provider_with_invalid_email():
    """Test updating provider with invalid email fails"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST"
    )

    with pytest.raises(ValueError, match="Invalid email format"):
        provider.update_info(email="invalid-email")


def test_deactivate_insurance_provider():
    """Test deactivating provider"""
    import time
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST"
    )

    assert provider.is_active is True

    original_updated_at = provider.updated_at
    time.sleep(0.01)  # Small delay to ensure different timestamp
    provider.deactivate()

    assert provider.is_active is False
    assert provider.updated_at >= original_updated_at


def test_activate_insurance_provider():
    """Test activating provider"""
    import time
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST"
    )

    provider.deactivate()
    assert provider.is_active is False

    original_updated_at = provider.updated_at
    time.sleep(0.01)  # Small delay to ensure different timestamp
    provider.activate()

    assert provider.is_active is True
    assert provider.updated_at >= original_updated_at


def test_insurance_provider_unique_ids():
    """Test that each provider gets a unique ID"""
    provider1 = InsuranceProvider.create(
        name="Insurance One",
        code="INS1"
    )
    provider2 = InsuranceProvider.create(
        name="Insurance Two",
        code="INS2"
    )

    assert provider1.id != provider2.id
