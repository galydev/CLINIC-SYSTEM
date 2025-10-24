"""Add emergency contact use case - Application layer business logic"""
import logging
from uuid import UUID

from application.dto.emergency_contact_request import \
    AddEmergencyContactRequest
from application.dto.emergency_contact_response import EmergencyContactResponse
from domain.entities.emergency_contact import EmergencyContact
from domain.repositories.catalog_repository import RelationshipTypeRepository
from domain.repositories.emergency_contact_repository import \
    EmergencyContactRepository
from domain.repositories.patient_repository import PatientRepository

logger = logging.getLogger(__name__)


class PatientNotFoundError(Exception):
    """Exception raised when patient is not found"""
    pass


class ValidationError(Exception):
    """Exception raised when emergency contact data validation fails"""
    pass


class AddEmergencyContactUseCase:

    def __init__(
        self,
        emergency_contact_repository: EmergencyContactRepository,
        patient_repository: PatientRepository,
        relationship_type_repository: RelationshipTypeRepository
    ):
        self.emergency_contact_repository = emergency_contact_repository
        self.patient_repository = patient_repository
        self.relationship_type_repository = relationship_type_repository

    async def execute(
        self,
        patient_id: UUID,
        request: AddEmergencyContactRequest
    ) -> EmergencyContactResponse:

        try:
            # Verify patient exists
            patient = await self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise PatientNotFoundError(f"Patient with ID {patient_id} not found")

            # Validate relationship type code exists in database
            relationship_type_id = await self.relationship_type_repository.get_by_code(request.relationship)
            if not relationship_type_id:
                raise ValidationError(f"Invalid relationship type code: {request.relationship}")

            # Create emergency contact entity with validated catalog code (as string)
            # EmergencyContact.create validates: full_name, phone (7-15 digits)
            emergency_contact = EmergencyContact.create(
                patient_id=patient_id,
                full_name=request.full_name,
                phone=request.phone,
                relationship=request.relationship
            )

            # Persist emergency contact with validated catalog ID
            created_contact = await self.emergency_contact_repository.save(
                emergency_contact,
                relationship_type_id=relationship_type_id
            )

            logger.info(
                f"Emergency contact added for patient {patient.national_id_number}: "
                f"{created_contact.full_name}"
            )

            return EmergencyContactResponse(
                id=created_contact.id,
                patient_id=created_contact.patient_id,
                full_name=created_contact.full_name,
                phone=created_contact.phone,
                relationship=created_contact.relationship,
                created_at=created_contact.created_at,
                updated_at=created_contact.updated_at
            )

        except ValueError as e:
            logger.error(f"Validation error while adding emergency contact: {str(e)}")
            raise ValidationError(str(e))
        except PatientNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while adding emergency contact: {str(e)}")
            raise
