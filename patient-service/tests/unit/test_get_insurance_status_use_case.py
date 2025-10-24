"""Unit tests for GetInsuranceStatusUseCase with mocks"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date, datetime
from uuid import uuid4

from application.use_cases.get_insurance_status import (
    GetInsuranceStatusUseCase,
    PatientNotFoundError
)
from domain.entities.patient import Patient
from domain.entities.insurance_policy import InsurancePolicy
from domain.enums import Gender, MaritalStatus


@pytest.fixture
def mock_insurance_policy_repository():
    """Mock InsurancePolicyRepository"""
    return AsyncMock()


@pytest.fixture
def mock_patient_repository():
    """Mock PatientRepository"""
    return AsyncMock()


@pytest.fixture
def use_case(
    mock_insurance_policy_repository,
    mock_patient_repository
):
    """Create GetInsuranceStatusUseCase with mocked dependencies"""
    return GetInsuranceStatusUseCase(
        insurance_policy_repository=mock_insurance_policy_repository,
        patient_repository=mock_patient_repository
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
def mock_active_policy(mock_patient):
    """Create a mock active insurance policy"""
    provider_id = uuid4()
    policy = InsurancePolicy.create(
        patient_id=mock_patient.id,
        provider_id=provider_id,
        policy_number="POL-2024-001",
        coverage_details="Full coverage",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )
    policy.id = uuid4()
    policy.status = "ACTIVE"
    policy.created_at = datetime.now()
    policy.updated_at = datetime.now()
    return policy


@pytest.fixture
def mock_expired_policy(mock_patient):
    """Create a mock expired insurance policy"""
    provider_id = uuid4()
    policy = InsurancePolicy.create(
        patient_id=mock_patient.id,
        provider_id=provider_id,
        policy_number="POL-2020-001",
        coverage_details="Full coverage",
        valid_from=date(2020, 1, 1),
        valid_until=date(2021, 12, 31)
    )
    policy.id = uuid4()
    policy.status = "EXPIRED"
    policy.created_at = datetime.now()
    policy.updated_at = datetime.now()
    return policy


@pytest.mark.asyncio
async def test_get_insurance_status_patient_not_found(
    use_case,
    mock_patient_repository
):
    """Test get insurance status fails when patient doesn't exist"""
    # Arrange
    patient_id = uuid4()
    mock_patient_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PatientNotFoundError, match="not found"):
        await use_case.execute(patient_id)


@pytest.mark.asyncio
async def test_get_insurance_status_with_active_policy(
    use_case,
    mock_patient,
    mock_active_policy,
    mock_patient_repository,
    mock_insurance_policy_repository
):
    """Test getting insurance status when patient has an active policy"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = [mock_active_policy]

    # Act
    response = await use_case.execute(mock_patient.id)

    # Assert
    assert response.patient_id == mock_patient.id
    assert response.has_active_insurance is True
    assert response.has_policy is True
    assert response.active_policy is not None
    assert response.active_policy.id == mock_active_policy.id
    assert response.active_policy.policy_number == mock_active_policy.policy_number
    assert response.active_policy.status == "ACTIVE"

    # Verify repository calls
    mock_patient_repository.get_by_id.assert_called_once_with(mock_patient.id)
    mock_insurance_policy_repository.get_by_patient_id.assert_called_once_with(mock_patient.id)


@pytest.mark.asyncio
async def test_get_insurance_status_with_expired_policy(
    use_case,
    mock_patient,
    mock_expired_policy,
    mock_patient_repository,
    mock_insurance_policy_repository
):
    """Test getting insurance status when patient has an expired policy"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = [mock_expired_policy]

    # Act
    response = await use_case.execute(mock_patient.id)

    # Assert
    assert response.patient_id == mock_patient.id
    assert response.has_active_insurance is False  # Not active because expired
    assert response.has_policy is True  # Still has a policy
    assert response.active_policy is None  # No active policy returned

    # Verify repository calls
    mock_patient_repository.get_by_id.assert_called_once_with(mock_patient.id)
    mock_insurance_policy_repository.get_by_patient_id.assert_called_once_with(mock_patient.id)


@pytest.mark.asyncio
async def test_get_insurance_status_without_policy(
    use_case,
    mock_patient,
    mock_patient_repository,
    mock_insurance_policy_repository
):
    """Test getting insurance status when patient has no policy"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = []  # No policies

    # Act
    response = await use_case.execute(mock_patient.id)

    # Assert
    assert response.patient_id == mock_patient.id
    assert response.has_active_insurance is False
    assert response.has_policy is False
    assert response.active_policy is None

    # Verify repository calls
    mock_patient_repository.get_by_id.assert_called_once_with(mock_patient.id)
    mock_insurance_policy_repository.get_by_patient_id.assert_called_once_with(mock_patient.id)


@pytest.mark.asyncio
async def test_get_insurance_status_updates_policy_status(
    use_case,
    mock_patient,
    mock_patient_repository,
    mock_insurance_policy_repository
):
    """Test that get insurance status calls update_status on the policy"""
    # Arrange
    provider_id = uuid4()
    policy = InsurancePolicy.create(
        patient_id=mock_patient.id,
        provider_id=provider_id,
        policy_number="POL-2024-001",
        coverage_details="Full coverage",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )
    policy.id = uuid4()
    policy.status = "PENDING"  # Initial status
    policy.created_at = datetime.now()
    policy.updated_at = datetime.now()

    # Mock the update_status method to change status to ACTIVE
    def update_status_side_effect():
        policy.status = "ACTIVE"

    policy.update_status = MagicMock(side_effect=update_status_side_effect)

    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = [policy]

    # Act
    response = await use_case.execute(mock_patient.id)

    # Assert
    policy.update_status.assert_called_once()
    assert response.has_active_insurance is True
    assert response.active_policy.status == "ACTIVE"


@pytest.mark.asyncio
async def test_get_insurance_status_only_returns_one_policy(
    use_case,
    mock_patient,
    mock_active_policy,
    mock_patient_repository,
    mock_insurance_policy_repository
):
    """Test that only ONE policy is returned (one policy per patient rule)"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    # Even if repository returns a list, we only process the first one
    mock_insurance_policy_repository.get_by_patient_id.return_value = [mock_active_policy]

    # Act
    response = await use_case.execute(mock_patient.id)

    # Assert
    assert response.active_policy is not None  # Single policy, not a list
    assert response.active_policy.id == mock_active_policy.id
    assert isinstance(response.active_policy.id, type(mock_active_policy.id))  # Single object


@pytest.mark.asyncio
async def test_get_insurance_status_suspended_policy(
    use_case,
    mock_patient,
    mock_patient_repository,
    mock_insurance_policy_repository
):
    """Test getting insurance status when policy is suspended"""
    # Arrange
    provider_id = uuid4()
    policy = InsurancePolicy.create(
        patient_id=mock_patient.id,
        provider_id=provider_id,
        policy_number="POL-2024-001",
        coverage_details="Full coverage",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )
    policy.id = uuid4()
    policy.status = "SUSPENDED"
    policy.created_at = datetime.now()
    policy.updated_at = datetime.now()

    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_insurance_policy_repository.get_by_patient_id.return_value = [policy]

    # Act
    response = await use_case.execute(mock_patient.id)

    # Assert
    assert response.patient_id == mock_patient.id
    assert response.has_active_insurance is False  # Not active because suspended
    assert response.has_policy is True  # Still has a policy
    assert response.active_policy is None  # No active policy returned
