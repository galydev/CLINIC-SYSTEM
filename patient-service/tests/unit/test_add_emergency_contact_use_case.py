"""Unit tests for AddEmergencyContactUseCase with mocks"""
import pytest
from unittest.mock import AsyncMock
from datetime import date
from uuid import uuid4

from application.use_cases.add_emergency_contact import (
    AddEmergencyContactUseCase,
    PatientNotFoundError,
    ValidationError
)
from application.dto.emergency_contact_request import AddEmergencyContactRequest
from domain.entities.patient import Patient
from domain.entities.emergency_contact import EmergencyContact
from domain.enums import Gender, MaritalStatus


@pytest.fixture
def mock_emergency_contact_repository():
    """Mock EmergencyContactRepository"""
    return AsyncMock()


@pytest.fixture
def mock_patient_repository():
    """Mock PatientRepository"""
    return AsyncMock()


@pytest.fixture
def mock_relationship_type_repository():
    """Mock RelationshipTypeRepository"""
    return AsyncMock()


@pytest.fixture
def use_case(
    mock_emergency_contact_repository,
    mock_patient_repository,
    mock_relationship_type_repository
):
    """Create AddEmergencyContactUseCase with mocked dependencies"""
    return AddEmergencyContactUseCase(
        emergency_contact_repository=mock_emergency_contact_repository,
        patient_repository=mock_patient_repository,
        relationship_type_repository=mock_relationship_type_repository
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
def valid_contact_request():
    """Create a valid emergency contact request"""
    return AddEmergencyContactRequest(
        full_name="Jane Doe",
        phone="9876543210",
        relationship="SPOUSE"
    )


@pytest.mark.asyncio
async def test_add_emergency_contact_success(
    use_case,
    mock_patient,
    valid_contact_request,
    mock_patient_repository,
    mock_relationship_type_repository,
    mock_emergency_contact_repository
):
    """Test successful emergency contact addition"""
    # Arrange
    contact_id = uuid4()
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_relationship_type_repository.get_by_code.return_value = 1  # SPOUSE relationship ID

    # Create mock emergency contact
    created_contact = EmergencyContact.create(
        patient_id=mock_patient.id,
        full_name=valid_contact_request.full_name,
        phone=valid_contact_request.phone,
        relationship=valid_contact_request.relationship
    )
    created_contact.id = contact_id

    mock_emergency_contact_repository.save.return_value = created_contact

    # Act
    response = await use_case.execute(mock_patient.id, valid_contact_request)

    # Assert
    assert response.id == contact_id
    assert response.patient_id == mock_patient.id
    assert response.full_name == valid_contact_request.full_name
    assert response.phone == valid_contact_request.phone
    assert response.relationship == valid_contact_request.relationship

    # Verify repository calls
    mock_patient_repository.get_by_id.assert_called_once_with(mock_patient.id)
    mock_relationship_type_repository.get_by_code.assert_called_once_with(
        valid_contact_request.relationship
    )
    mock_emergency_contact_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_add_emergency_contact_patient_not_found(
    use_case,
    valid_contact_request,
    mock_patient_repository
):
    """Test adding contact fails when patient doesn't exist"""
    # Arrange
    patient_id = uuid4()
    mock_patient_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PatientNotFoundError, match="not found"):
        await use_case.execute(patient_id, valid_contact_request)

    # Verify save was not called
    mock_patient_repository.get_by_id.assert_called_once_with(patient_id)


@pytest.mark.asyncio
async def test_add_emergency_contact_invalid_relationship(
    use_case,
    mock_patient,
    valid_contact_request,
    mock_patient_repository,
    mock_relationship_type_repository,
    mock_emergency_contact_repository
):
    """Test adding contact fails when relationship type is invalid"""
    # Arrange
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_relationship_type_repository.get_by_code.return_value = None  # Invalid

    # Act & Assert
    with pytest.raises(ValidationError, match="Invalid relationship type code"):
        await use_case.execute(mock_patient.id, valid_contact_request)

    # Verify save was not called
    mock_emergency_contact_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_emergency_contact_with_parent_relationship(
    use_case,
    mock_patient,
    mock_patient_repository,
    mock_relationship_type_repository,
    mock_emergency_contact_repository
):
    """Test adding contact with PARENT relationship"""
    # Arrange
    contact_request = AddEmergencyContactRequest(
        full_name="Maria Doe",
        phone="5551234567",
        relationship="PARENT"
    )

    contact_id = uuid4()
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_relationship_type_repository.get_by_code.return_value = 2  # PARENT relationship ID

    created_contact = EmergencyContact.create(
        patient_id=mock_patient.id,
        full_name=contact_request.full_name,
        phone=contact_request.phone,
        relationship=contact_request.relationship
    )
    created_contact.id = contact_id

    mock_emergency_contact_repository.save.return_value = created_contact

    # Act
    response = await use_case.execute(mock_patient.id, contact_request)

    # Assert
    assert response.relationship == "PARENT"
    mock_relationship_type_repository.get_by_code.assert_called_once_with("PARENT")


@pytest.mark.asyncio
async def test_add_emergency_contact_with_sibling_relationship(
    use_case,
    mock_patient,
    mock_patient_repository,
    mock_relationship_type_repository,
    mock_emergency_contact_repository
):
    """Test adding contact with SIBLING relationship"""
    # Arrange
    contact_request = AddEmergencyContactRequest(
        full_name="Robert Doe",
        phone="5559876543",
        relationship="SIBLING"
    )

    contact_id = uuid4()
    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_relationship_type_repository.get_by_code.return_value = 3  # SIBLING relationship ID

    created_contact = EmergencyContact.create(
        patient_id=mock_patient.id,
        full_name=contact_request.full_name,
        phone=contact_request.phone,
        relationship=contact_request.relationship
    )
    created_contact.id = contact_id

    mock_emergency_contact_repository.save.return_value = created_contact

    # Act
    response = await use_case.execute(mock_patient.id, contact_request)

    # Assert
    assert response.relationship == "SIBLING"
    mock_relationship_type_repository.get_by_code.assert_called_once_with("SIBLING")


@pytest.mark.asyncio
async def test_add_emergency_contact_multiple_contacts_same_patient(
    use_case,
    mock_patient,
    mock_patient_repository,
    mock_relationship_type_repository,
    mock_emergency_contact_repository
):
    """Test adding multiple emergency contacts for the same patient"""
    # Arrange - First contact
    contact1_request = AddEmergencyContactRequest(
        full_name="Jane Doe",
        phone="1111111111",
        relationship="SPOUSE"
    )

    # Arrange - Second contact
    contact2_request = AddEmergencyContactRequest(
        full_name="Maria Doe",
        phone="2222222222",
        relationship="PARENT"
    )

    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_relationship_type_repository.get_by_code.side_effect = [1, 2]  # Different IDs

    contact1 = EmergencyContact.create(
        patient_id=mock_patient.id,
        full_name=contact1_request.full_name,
        phone=contact1_request.phone,
        relationship=contact1_request.relationship
    )
    contact1.id = uuid4()

    contact2 = EmergencyContact.create(
        patient_id=mock_patient.id,
        full_name=contact2_request.full_name,
        phone=contact2_request.phone,
        relationship=contact2_request.relationship
    )
    contact2.id = uuid4()

    mock_emergency_contact_repository.save.side_effect = [contact1, contact2]

    # Act
    response1 = await use_case.execute(mock_patient.id, contact1_request)
    response2 = await use_case.execute(mock_patient.id, contact2_request)

    # Assert
    assert response1.full_name == "Jane Doe"
    assert response2.full_name == "Maria Doe"
    assert response1.id != response2.id
    assert mock_emergency_contact_repository.save.call_count == 2
