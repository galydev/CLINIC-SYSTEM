"""Unit tests for Patient entity"""
import pytest
from datetime import date, datetime
from domain.entities.patient import Patient
from domain.enums import Gender, BloodType, MaritalStatus


def test_create_patient_with_valid_data():
    """Test creating a patient with valid data"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St",
        blood_type=BloodType.O_POSITIVE,
        occupation="Engineer"
    )

    assert patient.national_id_number == "1234567890"
    assert patient.full_name == "John Doe"
    assert patient.email == "john.doe@example.com"
    assert patient.is_active is True


def test_create_patient_with_invalid_national_id():
    """Test creating a patient with invalid national ID (too short)"""
    with pytest.raises(ValueError, match="National ID number must be between 6 and 10 digits"):
        Patient.create(
            national_id_number="12345",  # Too short
            full_name="John Doe",
            birth_date=date(1990, 1, 15),
            gender=Gender.MALE,
            marital_status=MaritalStatus.SINGLE,
            phone="1234567890",
            email="john.doe@example.com",
            address="123 Main St"
        )


def test_create_patient_with_invalid_email():
    """Test creating a patient with invalid email format"""
    with pytest.raises(ValueError, match="Invalid email format"):
        Patient.create(
            national_id_number="1234567890",
            full_name="John Doe",
            birth_date=date(1990, 1, 15),
            gender=Gender.MALE,
            marital_status=MaritalStatus.SINGLE,
            phone="1234567890",
            email="invalid-email",  # Invalid format
            address="123 Main St"
        )


def test_create_patient_with_invalid_phone():
    """Test creating a patient with invalid phone (too short)"""
    with pytest.raises(ValueError, match="Phone must be between 7 and 15 digits"):
        Patient.create(
            national_id_number="1234567890",
            full_name="John Doe",
            birth_date=date(1990, 1, 15),
            gender=Gender.MALE,
            marital_status=MaritalStatus.SINGLE,
            phone="123",  # Too short
            email="john.doe@example.com",
            address="123 Main St"
        )


def test_create_patient_with_future_birth_date():
    """Test creating a patient with birth date in the future"""
    future_date = date(2030, 1, 1)
    with pytest.raises(ValueError, match="Birth date cannot be in the future"):
        Patient.create(
            national_id_number="1234567890",
            full_name="John Doe",
            birth_date=future_date,
            gender=Gender.MALE,
            marital_status=MaritalStatus.SINGLE,
            phone="1234567890",
            email="john.doe@example.com",
            address="123 Main St"
        )


def test_create_patient_too_old():
    """Test creating a patient older than 150 years"""
    old_date = date(1800, 1, 1)
    with pytest.raises(ValueError, match="Age cannot exceed 150 years"):
        Patient.create(
            national_id_number="1234567890",
            full_name="John Doe",
            birth_date=old_date,
            gender=Gender.MALE,
            marital_status=MaritalStatus.SINGLE,
            phone="1234567890",
            email="john.doe@example.com",
            address="123 Main St"
        )


def test_update_patient_profile():
    """Test updating patient profile"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    patient.update_profile(
        full_name="John Updated Doe",
        phone="9876543210"
    )

    assert patient.full_name == "John Updated Doe"
    assert patient.phone == "9876543210"


def test_add_allergy():
    """Test adding allergy to patient"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    patient.add_allergy("Penicillin")
    assert "Penicillin" in patient.allergies


def test_get_age():
    """Test calculating patient age"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    age = patient.get_age()
    expected_age = date.today().year - 1990
    assert age in [expected_age - 1, expected_age]  # Account for birthday not passed yet


def test_add_allergy_empty():
    """Test adding empty allergy fails"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    with pytest.raises(ValueError, match="Allergy cannot be empty"):
        patient.add_allergy("")


def test_remove_allergy():
    """Test removing an allergy"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    patient.add_allergy("Penicillin")
    patient.add_allergy("Peanuts")
    assert "Penicillin" in patient.allergies
    assert "Peanuts" in patient.allergies

    patient.remove_allergy("Penicillin")
    assert "Penicillin" not in patient.allergies
    assert "Peanuts" in patient.allergies


def test_add_chronic_condition():
    """Test adding a chronic condition"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    patient.add_chronic_condition("Diabetes")
    assert "Diabetes" in patient.chronic_conditions


def test_add_chronic_condition_empty():
    """Test adding empty chronic condition fails"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    with pytest.raises(ValueError, match="Chronic condition cannot be empty"):
        patient.add_chronic_condition("")


def test_remove_chronic_condition():
    """Test removing a chronic condition"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    patient.add_chronic_condition("Diabetes")
    patient.add_chronic_condition("Hypertension")
    assert "Diabetes" in patient.chronic_conditions

    patient.remove_chronic_condition("Diabetes")
    assert "Diabetes" not in patient.chronic_conditions
    assert "Hypertension" in patient.chronic_conditions


def test_deactivate_patient():
    """Test deactivating patient"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    assert patient.is_active is True
    patient.deactivate()
    assert patient.is_active is False


def test_activate_patient():
    """Test activating patient"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    patient.deactivate()
    assert patient.is_active is False
    patient.activate()
    assert patient.is_active is True


def test_patient_to_dict():
    """Test converting patient to dictionary"""
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St",
        blood_type=BloodType.O_POSITIVE,
        occupation="Engineer",
        allergies=["Penicillin"],
        chronic_conditions=["Diabetes"]
    )

    patient_dict = patient.to_dict()

    assert patient_dict["id"] == str(patient.id)
    assert patient_dict["national_id_number"] == "1234567890"
    assert patient_dict["full_name"] == "John Doe"
    assert patient_dict["gender"] == "MALE"
    assert patient_dict["marital_status"] == "SINGLE"
    assert patient_dict["blood_type"] == BloodType.O_POSITIVE
    assert patient_dict["occupation"] == "Engineer"
    assert patient_dict["allergies"] == ["Penicillin"]
    assert patient_dict["chronic_conditions"] == ["Diabetes"]
    assert patient_dict["is_active"] is True
    assert "created_at" in patient_dict
    assert "updated_at" in patient_dict
