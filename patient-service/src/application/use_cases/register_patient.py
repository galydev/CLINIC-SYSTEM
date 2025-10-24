"""Register patient use case - Application layer business logic"""
import logging
from typing import Optional

from application.dto.patient_request import RegisterPatientRequest
from application.dto.patient_response import PatientResponse
from domain.entities.patient import Patient
from domain.repositories.catalog_repository import (BloodTypeRepository,
                                                    GenderRepository,
                                                    MaritalStatusRepository)
from domain.repositories.patient_repository import PatientRepository

logger = logging.getLogger(__name__)


class DuplicatePatientError(Exception):
    """Exception raised when trying to register a patient that already exists"""
    pass


class ValidationError(Exception):
    """Exception raised when patient data validation fails"""
    pass


class RegisterPatientUseCase:

    def __init__(
        self,
        patient_repository: PatientRepository,
        gender_repository: GenderRepository,
        blood_type_repository: BloodTypeRepository,
        marital_status_repository: MaritalStatusRepository
    ):
        self.patient_repository = patient_repository
        self.gender_repository = gender_repository
        self.blood_type_repository = blood_type_repository
        self.marital_status_repository = marital_status_repository

    async def execute(self, request: RegisterPatientRequest) -> PatientResponse:

        try:
            # Check national_id_number uniqueness
            existing_patient_by_national_id = await self.patient_repository.get_by_national_id_number(
                request.national_id_number
            )
            if existing_patient_by_national_id:
                raise DuplicatePatientError(
                    f"Patient with national ID number {request.national_id_number} already exists"
                )

            # Check email uniqueness (case-insensitive)
            existing_patient_by_email = await self.patient_repository.exists_by_email(
                request.email.lower()
            )
            if existing_patient_by_email:
                raise DuplicatePatientError(
                    f"Email {request.email} is already registered"
                )

            # Validate catalog codes exist in database
            gender_id = await self.gender_repository.get_by_code(request.gender)
            if not gender_id:
                raise ValidationError(f"Invalid gender code: {request.gender}")

            marital_status_id = await self.marital_status_repository.get_by_code(request.marital_status)
            if not marital_status_id:
                raise ValidationError(f"Invalid marital status code: {request.marital_status}")

            blood_type_id = None
            if request.blood_type:
                blood_type_id = await self.blood_type_repository.get_by_code(request.blood_type)
                if not blood_type_id:
                    raise ValidationError(f"Invalid blood type code: {request.blood_type}")

            
            patient = Patient.create(
                national_id_number=request.national_id_number,
                full_name=request.full_name,
                birth_date=request.birth_date,
                gender=request.gender,
                marital_status=request.marital_status,
                phone=request.phone,
                email=request.email,
                address=request.address,
                blood_type=request.blood_type,
                occupation=request.occupation,
                allergies=request.allergies,
                chronic_conditions=request.chronic_conditions
            )

            # Persist patient with validated catalog IDs
            created_patient = await self.patient_repository.save(
                patient,
                gender_id=gender_id,
                blood_type_id=blood_type_id,
                marital_status_id=marital_status_id
            )

            logger.info(f"Patient registered successfully: {created_patient.national_id_number}")

            return PatientResponse(
                id=created_patient.id,
                national_id_number=created_patient.national_id_number,
                full_name=created_patient.full_name,
                birth_date=created_patient.birth_date,
                age=created_patient.get_age(),
                gender=created_patient.gender,
                blood_type=created_patient.blood_type,
                marital_status=created_patient.marital_status,
                phone=created_patient.phone,
                email=created_patient.email,
                address=created_patient.address,
                occupation=created_patient.occupation,
                allergies=created_patient.allergies,
                chronic_conditions=created_patient.chronic_conditions,
                is_active=created_patient.is_active,
                created_at=created_patient.created_at,
                updated_at=created_patient.updated_at
            )

        except ValueError as e:
            logger.error(f"Validation error while registering patient: {str(e)}")
            raise ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error while registering patient: {str(e)}")
            raise
