"""Get patient use case - Application layer business logic"""
import logging
from typing import Optional
from uuid import UUID

from application.dto.patient_response import PatientResponse
from domain.repositories.patient_repository import PatientRepository

logger = logging.getLogger(__name__)


class PatientNotFoundError(Exception):
    """Exception raised when patient is not found"""
    pass


class GetPatientUseCase:

    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    async def execute_by_id(self, patient_id: UUID) -> PatientResponse:
        
        patient = await self.patient_repository.get_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(f"Patient with ID {patient_id} not found")

        logger.info(f"Patient retrieved by ID: {patient.national_id_number}")

        return PatientResponse(
            id=patient.id,
            national_id_number=patient.national_id_number,
            full_name=patient.full_name,
            birth_date=patient.birth_date,
            age=patient.get_age(),
            gender=patient.gender,
            blood_type=patient.blood_type,
            marital_status=patient.marital_status,
            phone=patient.phone,
            email=patient.email,
            address=patient.address,
            occupation=patient.occupation,
            allergies=patient.allergies,
            chronic_conditions=patient.chronic_conditions,
            is_active=patient.is_active,
            created_at=patient.created_at,
            updated_at=patient.updated_at
        )

    async def execute_by_national_id(self, national_id_number: str) -> PatientResponse:

        patient = await self.patient_repository.get_by_national_id_number(national_id_number)
        if not patient:
            raise PatientNotFoundError(
                f"Patient with national ID {national_id_number} not found"
            )

        logger.info(f"Patient retrieved by national ID: {patient.national_id_number}")

        return PatientResponse(
            id=patient.id,
            national_id_number=patient.national_id_number,
            full_name=patient.full_name,
            birth_date=patient.birth_date,
            age=patient.get_age(),
            gender=patient.gender,
            blood_type=patient.blood_type,
            marital_status=patient.marital_status,
            phone=patient.phone,
            email=patient.email,
            address=patient.address,
            occupation=patient.occupation,
            allergies=patient.allergies,
            chronic_conditions=patient.chronic_conditions,
            is_active=patient.is_active,
            created_at=patient.created_at,
            updated_at=patient.updated_at
        )
