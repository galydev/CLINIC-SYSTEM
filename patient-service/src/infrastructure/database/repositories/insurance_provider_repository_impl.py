"""Insurance Provider repository implementation - SQLAlchemy"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.entities.insurance_provider import InsuranceProvider
from domain.repositories.insurance_provider_repository import InsuranceProviderRepository
from infrastructure.database.models.insurance_provider_model import InsuranceProviderModel


class InsuranceProviderRepositoryImpl(InsuranceProviderRepository):
    """SQLAlchemy implementation of InsuranceProvider repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: InsuranceProviderModel) -> InsuranceProvider:
        """Convert database model to domain entity"""
        return InsuranceProvider(
            id=model.id,
            name=model.name,
            code=model.code,
            phone=model.phone,
            email=model.email,
            website=model.website,
            address=model.address,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def save(self, provider: InsuranceProvider) -> InsuranceProvider:
        """Save a new insurance provider"""
        model = InsuranceProviderModel(
            id=provider.id,
            name=provider.name,
            code=provider.code,
            phone=provider.phone,
            email=provider.email,
            website=provider.website,
            address=provider.address,
            is_active=provider.is_active,
            created_at=provider.created_at,
            updated_at=provider.updated_at
        )

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, provider_id: UUID) -> Optional[InsuranceProvider]:
        """Get insurance provider by ID"""
        result = await self.session.execute(
            select(InsuranceProviderModel)
            .where(InsuranceProviderModel.id == provider_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_code(self, code: str) -> Optional[InsuranceProvider]:
        """Get insurance provider by code"""
        result = await self.session.execute(
            select(InsuranceProviderModel)
            .where(InsuranceProviderModel.code == code.upper())
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, active_only: bool = True) -> List[InsuranceProvider]:
        """Get all insurance providers"""
        query = select(InsuranceProviderModel)

        if active_only:
            query = query.where(InsuranceProviderModel.is_active == True)

        query = query.order_by(InsuranceProviderModel.name)

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, provider: InsuranceProvider) -> InsuranceProvider:
        """Update an existing insurance provider"""
        result = await self.session.execute(
            select(InsuranceProviderModel)
            .where(InsuranceProviderModel.id == provider.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.name = provider.name
            model.code = provider.code
            model.phone = provider.phone
            model.email = provider.email
            model.website = provider.website
            model.address = provider.address
            model.is_active = provider.is_active
            model.updated_at = provider.updated_at

            await self.session.commit()
            await self.session.refresh(model)
            return self._to_entity(model)

        return provider

    async def delete(self, provider_id: UUID) -> bool:
        """Delete an insurance provider (soft delete)"""
        result = await self.session.execute(
            select(InsuranceProviderModel)
            .where(InsuranceProviderModel.id == provider_id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.is_active = False
            await self.session.commit()
            return True

        return False

    async def exists_by_code(self, code: str) -> bool:
        """Check if insurance provider exists by code"""
        result = await self.session.execute(
            select(InsuranceProviderModel)
            .where(InsuranceProviderModel.code == code.upper())
        )
        return result.scalar_one_or_none() is not None
