"""Emergency Contact repository implementation - SQLAlchemy"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from domain.entities.emergency_contact import EmergencyContact
from domain.repositories.emergency_contact_repository import EmergencyContactRepository
from infrastructure.database.models.emergency_contact_model import EmergencyContactModel


class EmergencyContactRepositoryImpl(EmergencyContactRepository):
    """SQLAlchemy implementation of EmergencyContact repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: EmergencyContactModel) -> EmergencyContact:
        """Convert database model to domain entity"""
        # Use catalog code directly as string
        return EmergencyContact(
            id=model.id,
            patient_id=model.patient_id,
            full_name=model.full_name,
            phone=model.phone,
            relationship=model.relationship_type.code if model.relationship_type else None,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def save(self, emergency_contact: EmergencyContact, relationship_type_id: UUID) -> EmergencyContact:
        """Save a new emergency contact with catalog ID"""
        model = EmergencyContactModel(
            id=emergency_contact.id,
            patient_id=emergency_contact.patient_id,
            full_name=emergency_contact.full_name,
            phone=emergency_contact.phone,
            relationship_type_id=relationship_type_id,
            created_at=emergency_contact.created_at,
            updated_at=emergency_contact.updated_at
        )
        self.session.add(model)
        await self.session.commit()

        # Refresh with relationship loaded
        await self.session.refresh(model, ["relationship_type"])
        return self._to_entity(model)

    async def get_by_id(self, contact_id: UUID) -> Optional[EmergencyContact]:
        """Get emergency contact by ID"""
        result = await self.session.execute(
            select(EmergencyContactModel)
            .options(selectinload(EmergencyContactModel.relationship_type))
            .where(EmergencyContactModel.id == contact_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_patient_id(self, patient_id: UUID) -> List[EmergencyContact]:
        """Get all emergency contacts for a patient"""
        result = await self.session.execute(
            select(EmergencyContactModel)
            .options(selectinload(EmergencyContactModel.relationship_type))
            .where(EmergencyContactModel.patient_id == patient_id)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, emergency_contact: EmergencyContact, relationship_type_id: UUID) -> EmergencyContact:
        """Update an existing emergency contact with catalog ID"""
        result = await self.session.execute(
            select(EmergencyContactModel)
            .options(selectinload(EmergencyContactModel.relationship_type))
            .where(EmergencyContactModel.id == emergency_contact.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.full_name = emergency_contact.full_name
            model.phone = emergency_contact.phone
            model.relationship_type_id = relationship_type_id
            model.updated_at = emergency_contact.updated_at

            await self.session.commit()
            await self.session.refresh(model, ["relationship_type"])
            return self._to_entity(model)

        return emergency_contact

    async def delete(self, contact_id: UUID) -> bool:
        """Delete an emergency contact"""
        result = await self.session.execute(
            select(EmergencyContactModel).where(EmergencyContactModel.id == contact_id)
        )
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.commit()
            return True

        return False
