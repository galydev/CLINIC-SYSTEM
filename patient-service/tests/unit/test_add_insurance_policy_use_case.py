"""Unit tests for AddInsurancePolicyUseCase with mocks"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date
from uuid import uuid4

from application.use_cases.add_insurance_policy import (
    AddInsurancePolicyUseCase,
    PatientNotFoundError,
    InsuranceProviderNotFoundError,
    DuplicatePolicyError,
    ValidationError
)
from application.dto.insurance_policy_request import AddInsurancePolicyRequest
from domain.entities.insurance_policy import InsurancePolicy
from domain.entities.patient import Patient
from domain.entities.insurance_provider import InsuranceProvider
from domain.enums import Gender, MaritalStatus


@pytest.fixture
def mock_insurance_policy_repository():
    """Mock InsurancePolicyRepository"""
    return AsyncMock()


@pytest.fixture
def mock_insurance_provider_repository():
    """Mock InsuranceProviderRepository"""
    return AsyncMock()


@pytest.fixture
def mock_patient_repository():
    """Mock PatientRepository"""
    return AsyncMock()


@pytest.fixture
def mock_insurance_status_repository():
    """Mock InsuranceStatusRepository"""
    return AsyncMock()


@pytest.fixture
def use_case(
    mock_insurance_policy_repository,
    mock_insurance_provider_repository,
    mock_patient_repository,
    mock_insurance_status_repository
):
    """Create AddInsurancePolicyUseCase with mocked dependencies"""
    return AddInsurancePolicyUseCase(
        insurance_policy_repository=mock_insurance_policy_repository,
        insurance_provider_repository=mock_insurance_provider_repository,
        patient_repository=mock_patient_repository,
        insurance_status_repository=mock_insurance_status_repository
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
        address="123 Main St"
    )
    patient.id = uuid4()
    return patient


@pytest.fixture
def mock_provider():
    """Create a mock insurance provider"""
    provider = InsuranceProvider.create(
        name="Test Insurance",
        code="TEST001"
    )
    provider.id = uuid4()
    return provider


@pytest.fixture
def valid_policy_request(mock_provider):
    """Create a valid insurance policy request"""
    return AddInsurancePolicyRequest(
        provider_id=mock_provider.id,
        policy_number="POL-2024-001",
        coverage_details="Full coverage including dental and vision",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )


@pytest.mark.asyncio
async def test_add_insurance_policy_success(
    use_case,
    valid_policy_request,
    mock_patient,
    mock_provider,
    mock_patient_repository,
    mock_insurance_provider_repository,
    mock_insurance_policy_repository,
    mock_insurance_status_repository
):
    """Test successful insurance policy addition"""
    # Arrange
    policy_id = uuid4()
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = []  # No existing policies
    mock_insurance_provider_repository.get_by_id.return_value = mock_provider
    mock_insurance_policy_repository.exists_by_policy_number.return_value = False
    mock_insurance_status_repository.get_by_code.return_value = 1  # ACTIVE status

    # Create mock policy
    created_policy = InsurancePolicy.create(
        patient_id=mock_patient.id,
        provider_id=mock_provider.id,
        policy_number=valid_policy_request.policy_number,
        coverage_details=valid_policy_request.coverage_details,
        valid_from=valid_policy_request.valid_from,
        valid_until=valid_policy_request.valid_until
    )
    created_policy.id = policy_id
    created_policy.status = "ACTIVE"

    mock_insurance_policy_repository.save.return_value = created_policy

    # Act
    response = await use_case.execute(mock_patient.id, valid_policy_request)

    # Assert
    assert response.id == policy_id
    assert response.patient_id == mock_patient.id
    assert response.provider_id == mock_provider.id
    assert response.policy_number == valid_policy_request.policy_number
    assert response.status == "ACTIVE"

    # Verify repository calls
    mock_patient_repository.get_by_id.assert_called_once_with(mock_patient.id)
    mock_insurance_policy_repository.get_by_patient_id.assert_called_once_with(mock_patient.id)
    mock_insurance_provider_repository.get_by_id.assert_called_once_with(
        valid_policy_request.provider_id
    )
    mock_insurance_policy_repository.exists_by_policy_number.assert_called_once_with(
        valid_policy_request.policy_number
    )
    mock_insurance_status_repository.get_by_code.assert_called_once_with('ACTIVE')
    mock_insurance_policy_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_add_insurance_policy_patient_not_found(
    use_case,
    valid_policy_request,
    mock_patient_repository
):
    """Test adding policy fails when patient doesn't exist"""
    # Arrange
    patient_id = uuid4()
    mock_patient_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PatientNotFoundError, match="not found"):
        await use_case.execute(patient_id, valid_policy_request)

    # Verify save was not called
    mock_patient_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_insurance_policy_patient_already_has_policy(
    use_case,
    valid_policy_request,
    mock_patient,
    mock_patient_repository,
    mock_insurance_policy_repository
):
    """Test adding policy fails when patient already has a policy (ONE POLICY PER PATIENT)"""
    # Arrange
    existing_policy = MagicMock()
    existing_policy.id = uuid4()
    existing_policy.policy_number = "EXISTING-001"

    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = [existing_policy]

    # Act & Assert
    with pytest.raises(DuplicatePolicyError, match="already has an insurance policy"):
        await use_case.execute(mock_patient.id, valid_policy_request)

    # Verify save was not called
    mock_insurance_policy_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_insurance_policy_provider_not_found(
    use_case,
    valid_policy_request,
    mock_patient,
    mock_patient_repository,
    mock_insurance_policy_repository,
    mock_insurance_provider_repository
):
    """Test adding policy fails when insurance provider doesn't exist"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = []
    mock_insurance_provider_repository.get_by_id.return_value = None  # Not found

    # Act & Assert
    with pytest.raises(InsuranceProviderNotFoundError, match="not found"):
        await use_case.execute(mock_patient.id, valid_policy_request)

    # Verify save was not called
    mock_insurance_policy_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_insurance_policy_duplicate_policy_number(
    use_case,
    valid_policy_request,
    mock_patient,
    mock_provider,
    mock_patient_repository,
    mock_insurance_policy_repository,
    mock_insurance_provider_repository
):
    """Test adding policy fails when policy number already exists"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = []
    mock_insurance_provider_repository.get_by_id.return_value = mock_provider
    mock_insurance_policy_repository.exists_by_policy_number.return_value = True  # Duplicate

    # Act & Assert
    with pytest.raises(DuplicatePolicyError, match="already exists"):
        await use_case.execute(mock_patient.id, valid_policy_request)

    # Verify save was not called
    mock_insurance_policy_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_insurance_policy_invalid_status(
    use_case,
    valid_policy_request,
    mock_patient,
    mock_provider,
    mock_patient_repository,
    mock_insurance_policy_repository,
    mock_insurance_provider_repository,
    mock_insurance_status_repository
):
    """Test adding policy fails when status code is invalid"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = []
    mock_insurance_provider_repository.get_by_id.return_value = mock_provider
    mock_insurance_policy_repository.exists_by_policy_number.return_value = False
    mock_insurance_status_repository.get_by_code.return_value = None  # Invalid

    # Act & Assert
    with pytest.raises(ValidationError, match="Invalid insurance status code"):
        await use_case.execute(mock_patient.id, valid_policy_request)

    # Verify save was not called
    mock_insurance_policy_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_insurance_policy_invalid_dates(
    use_case,
    mock_patient,
    mock_provider,
    mock_patient_repository,
    mock_insurance_policy_repository,
    mock_insurance_provider_repository,
    mock_insurance_status_repository
):
    """Test adding policy fails when valid_from is after valid_until"""
    # Arrange
    invalid_request = AddInsurancePolicyRequest(
        provider_id=mock_provider.id,
        policy_number="POL-2024-001",
        coverage_details="Full coverage",
        valid_from=date(2025, 12, 31),  # After valid_until
        valid_until=date(2024, 1, 1)
    )

    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = []
    mock_insurance_provider_repository.get_by_id.return_value = mock_provider
    mock_insurance_policy_repository.exists_by_policy_number.return_value = False
    mock_insurance_status_repository.get_by_code.return_value = 1

    # Act & Assert
    with pytest.raises(ValidationError, match="Valid from date must be before valid until date"):
        await use_case.execute(mock_patient.id, invalid_request)

    # Verify save was not called
    mock_insurance_policy_repository.save.assert_not_called()


