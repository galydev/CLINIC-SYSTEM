"""Unit tests for RegisterPatientUseCase with mocks"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date
from uuid import uuid4

from application.use_cases.register_patient import (
    RegisterPatientUseCase,
    DuplicatePatientError,
    ValidationError
)
from application.dto.patient_request import RegisterPatientRequest
from domain.entities.patient import Patient
from domain.enums import Gender, BloodType, MaritalStatus


@pytest.fixture
def mock_patient_repository():
    """Mock PatientRepository"""
    return AsyncMock()


@pytest.fixture
def mock_gender_repository():
    """Mock GenderRepository"""
    return AsyncMock()


@pytest.fixture
def mock_blood_type_repository():
    """Mock BloodTypeRepository"""
    return AsyncMock()


@pytest.fixture
def mock_marital_status_repository():
    """Mock MaritalStatusRepository"""
    return AsyncMock()


@pytest.fixture
def use_case(
    mock_patient_repository,
    mock_gender_repository,
    mock_blood_type_repository,
    mock_marital_status_repository
):
    """Create RegisterPatientUseCase with mocked dependencies"""
    return RegisterPatientUseCase(
        patient_repository=mock_patient_repository,
        gender_repository=mock_gender_repository,
        blood_type_repository=mock_blood_type_repository,
        marital_status_repository=mock_marital_status_repository
    )


@pytest.fixture
def valid_patient_request():
    """Create a valid patient registration request"""
    return RegisterPatientRequest(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender="M",
        marital_status="S",
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St",
        blood_type="O+",
        occupation="Engineer",
        allergies=["Penicillin"],
        chronic_conditions=[]
    )


@pytest.mark.asyncio
async def test_register_patient_success(
    use_case,
    valid_patient_request,
    mock_patient_repository,
    mock_gender_repository,
    mock_blood_type_repository,
    mock_marital_status_repository
):
    """Test successful patient registration"""
    # Arrange
    patient_id = uuid4()
    mock_patient_repository.get_by_national_id_number.return_value = None
    mock_patient_repository.exists_by_email.return_value = False
    mock_gender_repository.get_by_code.return_value = 1
    mock_marital_status_repository.get_by_code.return_value = 2
    mock_blood_type_repository.get_by_code.return_value = 3

    # Create mock patient entity
    created_patient = Patient.create(
        national_id_number=valid_patient_request.national_id_number,
        full_name=valid_patient_request.full_name,
        birth_date=valid_patient_request.birth_date,
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone=valid_patient_request.phone,
        email=valid_patient_request.email,
        address=valid_patient_request.address,
        blood_type=BloodType.O_POSITIVE,
        occupation=valid_patient_request.occupation,
        allergies=valid_patient_request.allergies,
        chronic_conditions=valid_patient_request.chronic_conditions
    )
    created_patient.id = patient_id

    mock_patient_repository.save.return_value = created_patient

    # Act
    response = await use_case.execute(valid_patient_request)

    # Assert
    assert response.id == patient_id
    assert response.national_id_number == valid_patient_request.national_id_number
    assert response.full_name == valid_patient_request.full_name
    assert response.email == valid_patient_request.email
    assert response.is_active is True

    # Verify repository calls
    mock_patient_repository.get_by_national_id_number.assert_called_once_with(
        valid_patient_request.national_id_number
    )
    mock_patient_repository.exists_by_email.assert_called_once_with(
        valid_patient_request.email.lower()
    )
    mock_gender_repository.get_by_code.assert_called_once_with(valid_patient_request.gender)
    mock_marital_status_repository.get_by_code.assert_called_once_with(
        valid_patient_request.marital_status
    )
    mock_blood_type_repository.get_by_code.assert_called_once_with(
        valid_patient_request.blood_type
    )
    mock_patient_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_patient_duplicate_national_id(
    use_case,
    valid_patient_request,
    mock_patient_repository
):
    """Test registration fails when national ID already exists"""
    # Arrange
    existing_patient = MagicMock()
    existing_patient.national_id_number = valid_patient_request.national_id_number
    mock_patient_repository.get_by_national_id_number.return_value = existing_patient

    # Act & Assert
    with pytest.raises(DuplicatePatientError, match="already exists"):
        await use_case.execute(valid_patient_request)

    # Verify save was not called
    mock_patient_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_patient_duplicate_email(
    use_case,
    valid_patient_request,
    mock_patient_repository
):
    """Test registration fails when email already exists"""
    # Arrange
    mock_patient_repository.get_by_national_id_number.return_value = None
    mock_patient_repository.exists_by_email.return_value = True

    # Act & Assert
    with pytest.raises(DuplicatePatientError, match="already registered"):
        await use_case.execute(valid_patient_request)

    # Verify save was not called
    mock_patient_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_patient_invalid_gender(
    use_case,
    valid_patient_request,
    mock_patient_repository,
    mock_gender_repository
):
    """Test registration fails when gender code is invalid"""
    # Arrange
    mock_patient_repository.get_by_national_id_number.return_value = None
    mock_patient_repository.exists_by_email.return_value = False
    mock_gender_repository.get_by_code.return_value = None  # Invalid gender

    # Act & Assert
    with pytest.raises(ValidationError, match="Invalid gender code"):
        await use_case.execute(valid_patient_request)

    # Verify save was not called
    mock_patient_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_patient_invalid_marital_status(
    use_case,
    valid_patient_request,
    mock_patient_repository,
    mock_gender_repository,
    mock_marital_status_repository
):
    """Test registration fails when marital status code is invalid"""
    # Arrange
    mock_patient_repository.get_by_national_id_number.return_value = None
    mock_patient_repository.exists_by_email.return_value = False
    mock_gender_repository.get_by_code.return_value = 1
    mock_marital_status_repository.get_by_code.return_value = None  # Invalid

    # Act & Assert
    with pytest.raises(ValidationError, match="Invalid marital status code"):
        await use_case.execute(valid_patient_request)

    # Verify save was not called
    mock_patient_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_patient_invalid_blood_type(
    use_case,
    valid_patient_request,
    mock_patient_repository,
    mock_gender_repository,
    mock_marital_status_repository,
    mock_blood_type_repository
):
    """Test registration fails when blood type code is invalid"""
    # Arrange
    mock_patient_repository.get_by_national_id_number.return_value = None
    mock_patient_repository.exists_by_email.return_value = False
    mock_gender_repository.get_by_code.return_value = 1
    mock_marital_status_repository.get_by_code.return_value = 2
    mock_blood_type_repository.get_by_code.return_value = None  # Invalid

    # Act & Assert
    with pytest.raises(ValidationError, match="Invalid blood type code"):
        await use_case.execute(valid_patient_request)

    # Verify save was not called
    mock_patient_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_patient_without_blood_type(
    use_case,
    mock_patient_repository,
    mock_gender_repository,
    mock_blood_type_repository,
    mock_marital_status_repository
):
    """Test successful registration without blood type (optional field)"""
    # Arrange
    request = RegisterPatientRequest(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=date(1990, 1, 15),
        gender="M",
        marital_status="S",
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St",
        blood_type=None,  # Optional
        occupation="Engineer"
    )

    patient_id = uuid4()
    mock_patient_repository.get_by_national_id_number.return_value = None
    mock_patient_repository.exists_by_email.return_value = False
    mock_gender_repository.get_by_code.return_value = 1
    mock_marital_status_repository.get_by_code.return_value = 2

    created_patient = Patient.create(
        national_id_number=request.national_id_number,
        full_name=request.full_name,
        birth_date=request.birth_date,
        gender=Gender.MALE,
        marital_status=MaritalStatus.SINGLE,
        phone=request.phone,
        email=request.email,
        address=request.address,
        occupation=request.occupation
    )
    created_patient.id = patient_id

    mock_patient_repository.save.return_value = created_patient

    # Act
    response = await use_case.execute(request)

    # Assert
    assert response.id == patient_id
    assert response.blood_type is None

    # Verify blood_type_repository was not called
    mock_blood_type_repository.get_by_code.assert_not_called()


@pytest.mark.asyncio
async def test_register_patient_with_invalid_birth_date(
    use_case,
    mock_patient_repository,
    mock_gender_repository,
    mock_marital_status_repository
):
    """Test registration fails when domain validation fails (e.g., future birth date)"""
    # Arrange - Note: Pydantic validates email/phone format, so we test birth date instead
    future_date = date(2030, 1, 1)

    invalid_request = RegisterPatientRequest(
        national_id_number="1234567890",
        full_name="John Doe",
        birth_date=future_date,  # Future date
        gender="M",
        marital_status="S",
        phone="1234567890",
        email="john.doe@example.com",
        address="123 Main St"
    )

    mock_patient_repository.get_by_national_id_number.return_value = None
    mock_patient_repository.exists_by_email.return_value = False
    mock_gender_repository.get_by_code.return_value = 1
    mock_marital_status_repository.get_by_code.return_value = 2

    # Act & Assert
    with pytest.raises(ValidationError, match="Birth date cannot be in the future"):
        await use_case.execute(invalid_request)

    # Verify save was not called
    mock_patient_repository.save.assert_not_called()
