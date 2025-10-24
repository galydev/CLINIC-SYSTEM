"""Update patient use case - Application layer business logic"""
import logging
from uuid import UUID

from application.dto.patient_request import UpdatePatientRequest
from application.dto.patient_response import PatientResponse
from domain.repositories.catalog_repository import MaritalStatusRepository
from domain.repositories.patient_repository import PatientRepository

logger = logging.getLogger(__name__)


class PatientNotFoundError(Exception):
    """Exception raised when patient is not found"""
    pass


class ValidationError(Exception):
    """Exception raised when patient data validation fails"""
    pass


class UpdatePatientUseCase:

    def __init__(
        self,
        patient_repository: PatientRepository,
        marital_status_repository: MaritalStatusRepository
    ):
        self.patient_repository = patient_repository
        self.marital_status_repository = marital_status_repository

    async def execute(
        self,
        patient_id: UUID,
        request: UpdatePatientRequest
    ) -> PatientResponse:

        try:
            # Get existing patient
            patient = await self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise PatientNotFoundError(f"Patient with ID {patient_id} not found")

            # Validate marital status code exists in database
            marital_status_id = await self.marital_status_repository.get_by_code(request.marital_status)
            if not marital_status_id:
                raise ValidationError(f"Invalid marital status code: {request.marital_status}")

            # Update patient profile with validated catalog code (as string)
            # update_profile validates: full_name, phone, email, address, occupation
            patient.update_profile(
                full_name=request.full_name,
                phone=request.phone,
                email=request.email,
                address=request.address,
                marital_status=request.marital_status,
                occupation=request.occupation
            )

            # Persist changes with validated catalog ID
            updated_patient = await self.patient_repository.update(
                patient,
                marital_status_id=marital_status_id
            )

            logger.info(f"Patient updated successfully: {updated_patient.national_id_number}")

            return PatientResponse(
                id=updated_patient.id,
                national_id_number=updated_patient.national_id_number,
                full_name=updated_patient.full_name,
                birth_date=updated_patient.birth_date,
                age=updated_patient.get_age(),
                gender=updated_patient.gender,
                blood_type=updated_patient.blood_type,
                marital_status=updated_patient.marital_status,
                phone=updated_patient.phone,
                email=updated_patient.email,
                address=updated_patient.address,
                occupation=updated_patient.occupation,
                allergies=updated_patient.allergies,
                chronic_conditions=updated_patient.chronic_conditions,
                is_active=updated_patient.is_active,
                created_at=updated_patient.created_at,
                updated_at=updated_patient.updated_at
            )

        except ValueError as e:
            logger.error(f"Validation error while updating patient: {str(e)}")
            raise ValidationError(str(e))
        except PatientNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while updating patient: {str(e)}")
            raise
