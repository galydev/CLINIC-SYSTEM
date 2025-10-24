"""Unit tests for EmergencyContact entity"""
import pytest
from datetime import datetime
from uuid import uuid4

from domain.entities.emergency_contact import EmergencyContact


def test_create_emergency_contact_with_valid_data():
    """Test creating an emergency contact with valid data"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    assert contact.patient_id == patient_id
    assert contact.full_name == "Jane Doe"
    assert contact.phone == "1234567890"
    assert contact.relationship == "SPOUSE"
    assert contact.id is not None
    assert isinstance(contact.created_at, datetime)
    assert isinstance(contact.updated_at, datetime)


def test_create_emergency_contact_with_empty_name():
    """Test creating contact with empty name fails"""
    patient_id = uuid4()
    with pytest.raises(ValueError, match="Full name cannot be empty"):
        EmergencyContact.create(
            patient_id=patient_id,
            full_name="",
            phone="1234567890",
            relationship="SPOUSE"
        )


def test_create_emergency_contact_with_long_name():
    """Test creating contact with name too long fails"""
    patient_id = uuid4()
    with pytest.raises(ValueError, match="Full name must not exceed 100 characters"):
        EmergencyContact.create(
            patient_id=patient_id,
            full_name="A" * 101,
            phone="1234567890",
            relationship="SPOUSE"
        )


def test_create_emergency_contact_with_empty_phone():
    """Test creating contact with empty phone fails"""
    patient_id = uuid4()
    with pytest.raises(ValueError, match="Phone cannot be empty"):
        EmergencyContact.create(
            patient_id=patient_id,
            full_name="Jane Doe",
            phone="",
            relationship="SPOUSE"
        )


def test_create_emergency_contact_with_invalid_phone_non_digits():
    """Test creating contact with non-digit phone fails"""
    patient_id = uuid4()
    with pytest.raises(ValueError, match="Phone must contain only digits"):
        EmergencyContact.create(
            patient_id=patient_id,
            full_name="Jane Doe",
            phone="123-456-7890",
            relationship="SPOUSE"
        )


def test_create_emergency_contact_with_phone_too_short():
    """Test creating contact with phone too short fails"""
    patient_id = uuid4()
    with pytest.raises(ValueError, match="Phone must be between 7 and 15 digits"):
        EmergencyContact.create(
            patient_id=patient_id,
            full_name="Jane Doe",
            phone="123456",  # Too short
            relationship="SPOUSE"
        )


def test_create_emergency_contact_with_phone_too_long():
    """Test creating contact with phone too long fails"""
    patient_id = uuid4()
    with pytest.raises(ValueError, match="Phone must be between 7 and 15 digits"):
        EmergencyContact.create(
            patient_id=patient_id,
            full_name="Jane Doe",
            phone="1234567890123456",  # Too long
            relationship="SPOUSE"
        )


def test_create_emergency_contact_with_parent_relationship():
    """Test creating contact with PARENT relationship"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Maria Doe",
        phone="5551234567",
        relationship="PARENT"
    )

    assert contact.relationship == "PARENT"


def test_create_emergency_contact_with_sibling_relationship():
    """Test creating contact with SIBLING relationship"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Robert Doe",
        phone="5559876543",
        relationship="SIBLING"
    )

    assert contact.relationship == "SIBLING"


def test_create_emergency_contact_with_child_relationship():
    """Test creating contact with CHILD relationship"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Junior Doe",
        phone="5551111111",
        relationship="CHILD"
    )

    assert contact.relationship == "CHILD"


def test_create_emergency_contact_with_friend_relationship():
    """Test creating contact with FRIEND relationship"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Best Friend",
        phone="5552222222",
        relationship="FRIEND"
    )

    assert contact.relationship == "FRIEND"


def test_update_emergency_contact_full_name():
    """Test updating contact full name"""
    import time
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    original_updated_at = contact.updated_at
    time.sleep(0.01)  # Small delay to ensure different timestamp

    contact.update(full_name="Jane Smith")

    assert contact.full_name == "Jane Smith"
    assert contact.updated_at >= original_updated_at


def test_update_emergency_contact_phone():
    """Test updating contact phone"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    contact.update(phone="9876543210")

    assert contact.phone == "9876543210"


def test_update_emergency_contact_relationship():
    """Test updating contact relationship"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    contact.update(relationship="FRIEND")

    assert contact.relationship == "FRIEND"


def test_update_emergency_contact_multiple_fields():
    """Test updating multiple contact fields at once"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    contact.update(
        full_name="Jane Smith",
        phone="9876543210",
        relationship="FRIEND"
    )

    assert contact.full_name == "Jane Smith"
    assert contact.phone == "9876543210"
    assert contact.relationship == "FRIEND"


def test_update_emergency_contact_with_invalid_name():
    """Test updating contact with invalid name fails"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    with pytest.raises(ValueError, match="Full name must not exceed 100 characters"):
        contact.update(full_name="A" * 101)


def test_update_emergency_contact_with_invalid_phone():
    """Test updating contact with invalid phone fails"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    with pytest.raises(ValueError, match="Phone must be between 7 and 15 digits"):
        contact.update(phone="123")


def test_emergency_contact_to_dict():
    """Test converting contact to dictionary"""
    patient_id = uuid4()
    contact = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )

    contact_dict = contact.to_dict()

    assert contact_dict["id"] == str(contact.id)
    assert contact_dict["patient_id"] == str(patient_id)
    assert contact_dict["full_name"] == "Jane Doe"
    assert contact_dict["phone"] == "1234567890"
    assert contact_dict["relationship"] == "SPOUSE"
    assert "created_at" in contact_dict
    assert "updated_at" in contact_dict


def test_emergency_contact_unique_ids():
    """Test that each contact gets a unique ID"""
    patient_id = uuid4()
    contact1 = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Jane Doe",
        phone="1234567890",
        relationship="SPOUSE"
    )
    contact2 = EmergencyContact.create(
        patient_id=patient_id,
        full_name="Maria Doe",
        phone="9876543210",
        relationship="PARENT"
    )

    assert contact1.id != contact2.id
