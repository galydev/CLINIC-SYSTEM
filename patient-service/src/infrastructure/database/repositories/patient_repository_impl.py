"""Patient repository implementation - SQLAlchemy"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from domain.entities.patient import Patient
from domain.repositories.patient_repository import PatientRepository
from infrastructure.database.models.patient_model import PatientModel
from infrastructure.database.models import (
    GenderModel,
    BloodTypeModel,
    MaritalStatusModel
)


class PatientRepositoryImpl(PatientRepository):
    """SQLAlchemy implementation of Patient repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: PatientModel) -> Patient:
        """Convert database model to domain entity"""
        # Use catalog codes directly as strings
        return Patient(
            id=model.id,
            national_id_number=model.national_id_number,
            full_name=model.full_name,
            birth_date=model.birth_date,
            gender=model.gender.code if model.gender else None,
            blood_type=model.blood_type.code if model.blood_type else None,
            marital_status=model.marital_status.code if model.marital_status else None,
            phone=model.phone,
            email=model.email,
            address=model.address,
            occupation=model.occupation,
            allergies=model.allergies or [],
            chronic_conditions=model.chronic_conditions or [],
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


    async def save(self, patient: Patient, gender_id: UUID, blood_type_id: Optional[UUID], marital_status_id: UUID) -> Patient:
        """Save a new patient with catalog IDs"""
        model = PatientModel(
            id=patient.id,
            national_id_number=patient.national_id_number,
            full_name=patient.full_name,
            birth_date=patient.birth_date,
            gender_id=gender_id,
            blood_type_id=blood_type_id,
            marital_status_id=marital_status_id,
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

        self.session.add(model)
        await self.session.commit()

        # Refresh with relationships loaded
        await self.session.refresh(model, ["gender", "blood_type", "marital_status"])
        return self._to_entity(model)

    async def get_by_id(self, patient_id: UUID) -> Optional[Patient]:
        """Get patient by ID"""
        result = await self.session.execute(
            select(PatientModel)
            .options(
                selectinload(PatientModel.gender),
                selectinload(PatientModel.blood_type),
                selectinload(PatientModel.marital_status)
            )
            .where(PatientModel.id == patient_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_national_id_number(self, national_id_number: str) -> Optional[Patient]:
        """Get patient by national ID number"""
        result = await self.session.execute(
            select(PatientModel)
            .options(
                selectinload(PatientModel.gender),
                selectinload(PatientModel.blood_type),
                selectinload(PatientModel.marital_status)
            )
            .where(PatientModel.national_id_number == national_id_number)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, patient: Patient, marital_status_id: UUID) -> Patient:
        """Update an existing patient with catalog IDs"""
        result = await self.session.execute(
            select(PatientModel)
            .options(
                selectinload(PatientModel.gender),
                selectinload(PatientModel.blood_type),
                selectinload(PatientModel.marital_status)
            )
            .where(PatientModel.id == patient.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.full_name = patient.full_name
            model.phone = patient.phone
            model.email = patient.email
            model.address = patient.address
            model.marital_status_id = marital_status_id
            model.occupation = patient.occupation
            model.allergies = patient.allergies
            model.chronic_conditions = patient.chronic_conditions
            model.is_active = patient.is_active
            model.updated_at = patient.updated_at

            await self.session.commit()
            await self.session.refresh(model, ["gender", "blood_type", "marital_status"])
            return self._to_entity(model)

        return patient

    async def delete(self, patient_id: UUID) -> bool:
        """Delete a patient (soft delete)"""
        result = await self.session.execute(
            select(PatientModel).where(PatientModel.id == patient_id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.is_active = False
            await self.session.commit()
            return True

        return False

    async def exists_by_national_id_number(self, national_id_number: str) -> bool:
        """Check if patient exists by national ID number"""
        result = await self.session.execute(
            select(PatientModel).where(
                PatientModel.national_id_number == national_id_number
            )
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_email(self, email: str) -> bool:
        """Check if patient exists by email"""
        result = await self.session.execute(
            select(PatientModel).where(PatientModel.email == email.lower())
        )
        return result.scalar_one_or_none() is not None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Get all patients with pagination"""
        result = await self.session.execute(
            select(PatientModel)
            .options(
                selectinload(PatientModel.gender),
                selectinload(PatientModel.blood_type),
                selectinload(PatientModel.marital_status)
            )
            .where(PatientModel.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Search patients by name"""
        result = await self.session.execute(
            select(PatientModel)
            .options(
                selectinload(PatientModel.gender),
                selectinload(PatientModel.blood_type),
                selectinload(PatientModel.marital_status)
            )
            .where(
                PatientModel.is_active == True,
                PatientModel.full_name.ilike(f"%{name}%")
            )
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
