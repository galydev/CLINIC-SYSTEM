"""Unit tests for GetPatientUseCase with mocks"""
import pytest
from unittest.mock import AsyncMock
from datetime import date
from uuid import uuid4

from application.use_cases.get_patient import (
    GetPatientUseCase,
    PatientNotFoundError
)
from domain.entities.patient import Patient
from domain.enums import Gender, BloodType, MaritalStatus


@pytest.fixture
def mock_patient_repository():
    """Mock PatientRepository"""
    return AsyncMock()


@pytest.fixture
def use_case(mock_patient_repository):
    """Create GetPatientUseCase with mocked dependencies"""
    return GetPatientUseCase(patient_repository=mock_patient_repository)


@pytest.fixture
def mock_patient():
    """Create a mock patient"""
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
    patient.id = uuid4()
    return patient


@pytest.mark.asyncio
async def test_get_patient_by_id_success(
    use_case,
    mock_patient,
    mock_patient_repository
):
    """Test successful patient retrieval by ID"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient

    # Act
    response = await use_case.execute_by_id(mock_patient.id)

    # Assert
    assert response.id == mock_patient.id
    assert response.national_id_number == mock_patient.national_id_number
    assert response.full_name == mock_patient.full_name
    assert response.email == mock_patient.email
    assert response.phone == mock_patient.phone
    assert response.is_active is True
    assert "Penicillin" in response.allergies
    assert "Diabetes" in response.chronic_conditions

    # Verify repository call
    mock_patient_repository.get_by_id.assert_called_once_with(mock_patient.id)


@pytest.mark.asyncio
async def test_get_patient_by_id_not_found(
    use_case,
    mock_patient_repository
):
    """Test get patient by ID fails when patient doesn't exist"""
    # Arrange
    patient_id = uuid4()
    mock_patient_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PatientNotFoundError, match="not found"):
        await use_case.execute_by_id(patient_id)

    # Verify repository call
    mock_patient_repository.get_by_id.assert_called_once_with(patient_id)


@pytest.mark.asyncio
async def test_get_patient_by_national_id_success(
    use_case,
    mock_patient,
    mock_patient_repository
):
    """Test successful patient retrieval by national ID"""
    # Arrange
    mock_patient_repository.get_by_national_id_number.return_value = mock_patient

    # Act
    response = await use_case.execute_by_national_id(mock_patient.national_id_number)

    # Assert
    assert response.id == mock_patient.id
    assert response.national_id_number == mock_patient.national_id_number
    assert response.full_name == mock_patient.full_name
    assert response.email == mock_patient.email
    assert response.is_active is True

    # Verify repository call
    mock_patient_repository.get_by_national_id_number.assert_called_once_with(
        mock_patient.national_id_number
    )


@pytest.mark.asyncio
async def test_get_patient_by_national_id_not_found(
    use_case,
    mock_patient_repository
):
    """Test get patient by national ID fails when patient doesn't exist"""
    # Arrange
    national_id = "9999999999"
    mock_patient_repository.get_by_national_id_number.return_value = None

    # Act & Assert
    with pytest.raises(PatientNotFoundError, match="not found"):
        await use_case.execute_by_national_id(national_id)

    # Verify repository call
    mock_patient_repository.get_by_national_id_number.assert_called_once_with(national_id)


@pytest.mark.asyncio
async def test_get_patient_by_id_returns_correct_age(
    use_case,
    mock_patient_repository
):
    """Test that patient response includes calculated age"""
    # Arrange
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
    patient.id = uuid4()

    mock_patient_repository.get_by_id.return_value = patient

    # Act
    response = await use_case.execute_by_id(patient.id)

    # Assert
    expected_age = date.today().year - 1990
    assert response.age in [expected_age - 1, expected_age]  # Account for birthday not passed yet


@pytest.mark.asyncio
async def test_get_patient_without_optional_fields(
    use_case,
    mock_patient_repository
):
    """Test retrieving patient without optional fields (blood_type, allergies, etc.)"""
    # Arrange
    patient = Patient.create(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
        # No blood_type, occupation, allergies, chronic_conditions
    )
    patient.id = uuid4()

    mock_patient_repository.get_by_id.return_value = patient

    # Act
    response = await use_case.execute_by_id(patient.id)

    # Assert
    assert response.id == patient.id
    assert response.blood_type is None
    assert response.occupation is None
    assert response.allergies == []
    assert response.chronic_conditions == []
