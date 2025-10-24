"""Catalog repository implementations - SQLAlchemy"""
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.repositories.catalog_repository import (
    GenderRepository,
    BloodTypeRepository,
    MaritalStatusRepository,
    RelationshipTypeRepository,
    InsuranceStatusRepository
)
from infrastructure.database.models import (
    GenderModel,
    BloodTypeModel,
    MaritalStatusModel,
    RelationshipTypeModel,
    InsuranceStatusModel
)


class GenderRepositoryImpl(GenderRepository):
    """SQLAlchemy implementation of Gender repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Optional[UUID]:
        """Get gender ID by code"""
        result = await self.session.execute(
            select(GenderModel.id)
            .where(GenderModel.code == code)
            .where(GenderModel.is_active == True)
        )
        gender_id = result.scalar_one_or_none()
        return gender_id


class BloodTypeRepositoryImpl(BloodTypeRepository):
    """SQLAlchemy implementation of BloodType repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Optional[UUID]:
        """Get blood type ID by code"""
        result = await self.session.execute(
            select(BloodTypeModel.id)
            .where(BloodTypeModel.code == code)
            .where(BloodTypeModel.is_active == True)
        )
        blood_type_id = result.scalar_one_or_none()
        return blood_type_id


class MaritalStatusRepositoryImpl(MaritalStatusRepository):
    """SQLAlchemy implementation of MaritalStatus repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Optional[UUID]:
        """Get marital status ID by code"""
        result = await self.session.execute(
            select(MaritalStatusModel.id)
            .where(MaritalStatusModel.code == code)
            .where(MaritalStatusModel.is_active == True)
        )
        marital_status_id = result.scalar_one_or_none()
        return marital_status_id


class RelationshipTypeRepositoryImpl(RelationshipTypeRepository):
    """SQLAlchemy implementation of RelationshipType repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Optional[UUID]:
        """Get relationship type ID by code"""
        result = await self.session.execute(
            select(RelationshipTypeModel.id)
            .where(RelationshipTypeModel.code == code)
            .where(RelationshipTypeModel.is_active == True)
        )
        relationship_type_id = result.scalar_one_or_none()
        return relationship_type_id


class InsuranceStatusRepositoryImpl(InsuranceStatusRepository):
    """SQLAlchemy implementation of InsuranceStatus repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Optional[UUID]:
        """Get insurance status ID by code"""
        result = await self.session.execute(
            select(InsuranceStatusModel.id)
            .where(InsuranceStatusModel.code == code)
            .where(InsuranceStatusModel.is_active == True)
        )
        insurance_status_id = result.scalar_one_or_none()
        return insurance_status_id
