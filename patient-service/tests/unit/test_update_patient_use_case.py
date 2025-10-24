"""Unit tests for UpdatePatientUseCase with mocks"""
import pytest
from unittest.mock import AsyncMock
from datetime import date
from uuid import uuid4

from application.use_cases.update_patient import (
    UpdatePatientUseCase,
    PatientNotFoundError,
    ValidationError
)
from application.dto.patient_request import UpdatePatientRequest
from domain.entities.patient import Patient
from domain.enums import Gender, BloodType, MaritalStatus


@pytest.fixture
def mock_patient_repository():
    """Mock PatientRepository"""
    return AsyncMock()


@pytest.fixture
def mock_marital_status_repository():
    """Mock MaritalStatusRepository"""
    return AsyncMock()


@pytest.fixture
def use_case(mock_patient_repository, mock_marital_status_repository):
    """Create UpdatePatientUseCase with mocked dependencies"""
    return UpdatePatientUseCase(
        patient_repository=mock_patient_repository,
        marital_status_repository=mock_marital_status_repository
    )


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
        occupation="Engineer"
    )
    patient.id = uuid4()
    return patient


@pytest.fixture
def valid_update_request():
    """Create a valid patient update request"""
    return UpdatePatientRequest(
        full_name="John Updated Doe",
        phone="9876543210",
        email="john.updated@example.com",
        address="456 New St",
        marital_status="M",
        occupation="Senior Engineer"
    )


@pytest.mark.asyncio
async def test_update_patient_success(
    use_case,
    mock_patient,
    valid_update_request,
    mock_patient_repository,
    mock_marital_status_repository
):
    """Test successful patient update"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_marital_status_repository.get_by_code.return_value = 2  # MARRIED status ID

    # Update patient attributes to reflect the update
    updated_patient = Patient.create(
        national_id_number=mock_patient.national_id_number,
        full_name=valid_update_request.full_name,
        birth_date=mock_patient.birth_date,
        gender=mock_patient.gender,
        marital_status=MaritalStatus.MARRIED,
        phone=valid_update_request.phone,
        email=valid_update_request.email,
        address=valid_update_request.address,
        blood_type=mock_patient.blood_type,
        occupation=valid_update_request.occupation
    )
    updated_patient.id = mock_patient.id

    mock_patient_repository.update.return_value = updated_patient

    # Act
    response = await use_case.execute(mock_patient.id, valid_update_request)

    # Assert
    assert response.id == mock_patient.id
    assert response.full_name == valid_update_request.full_name
    assert response.phone == valid_update_request.phone
    assert response.email == valid_update_request.email
    assert response.address == valid_update_request.address
    assert response.occupation == valid_update_request.occupation

    # Verify repository calls
    mock_patient_repository.get_by_id.assert_called_once_with(mock_patient.id)
    mock_marital_status_repository.get_by_code.assert_called_once_with(
        valid_update_request.marital_status
    )
    mock_patient_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_patient_not_found(
    use_case,
    valid_update_request,
    mock_patient_repository
):
    """Test update fails when patient doesn't exist"""
    # Arrange
    patient_id = uuid4()
    mock_patient_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PatientNotFoundError, match="not found"):
        await use_case.execute(patient_id, valid_update_request)

    # Verify update was not called
    mock_patient_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_update_patient_invalid_marital_status(
    use_case,
    mock_patient,
    valid_update_request,
    mock_patient_repository,
    mock_marital_status_repository
):
    """Test update fails when marital status code is invalid"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_marital_status_repository.get_by_code.return_value = None  # Invalid

    # Act & Assert
    with pytest.raises(ValidationError, match="Invalid marital status code"):
        await use_case.execute(mock_patient.id, valid_update_request)

    # Verify update was not called
    mock_patient_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_update_patient_partial_update(
    use_case,
    mock_patient,
    mock_patient_repository,
    mock_marital_status_repository
):
    """Test updating only some fields (partial update)"""
    # Arrange
    partial_request = UpdatePatientRequest(
        full_name="John Updated",
        phone=mock_patient.phone,  # Keep same
        email=mock_patient.email,  # Keep same
        address="New Address Only",
        marital_status="S",
        occupation=mock_patient.occupation  # Keep same
    )

    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_marital_status_repository.get_by_code.return_value = 1

    updated_patient = Patient.create(
        national_id_number=mock_patient.national_id_number,
        full_name=partial_request.full_name,
        birth_date=mock_patient.birth_date,
        gender=mock_patient.gender,
        marital_status=mock_patient.marital_status,
        phone=mock_patient.phone,
        email=mock_patient.email,
        address=partial_request.address,
        blood_type=mock_patient.blood_type,
        occupation=mock_patient.occupation
    )
    updated_patient.id = mock_patient.id

    mock_patient_repository.update.return_value = updated_patient

    # Act
    response = await use_case.execute(mock_patient.id, partial_request)

    # Assert
    assert response.full_name == "John Updated"
    assert response.address == "New Address Only"
    assert response.phone == mock_patient.phone  # Unchanged
    assert response.email == mock_patient.email  # Unchanged


