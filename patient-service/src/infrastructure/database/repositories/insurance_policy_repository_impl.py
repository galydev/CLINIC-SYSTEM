"""Insurance Policy repository implementation - SQLAlchemy"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from domain.entities.insurance_policy import InsurancePolicy
from domain.repositories.insurance_policy_repository import InsurancePolicyRepository
from infrastructure.database.models.insurance_policy_model import InsurancePolicyModel


class InsurancePolicyRepositoryImpl(InsurancePolicyRepository):
    """SQLAlchemy implementation of InsurancePolicy repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: InsurancePolicyModel) -> InsurancePolicy:
        """Convert database model to domain entity"""
        # Use catalog code directly as string
        return InsurancePolicy(
            id=model.id,
            patient_id=model.patient_id,
            provider_id=model.provider_id,
            policy_number=model.policy_number,
            coverage_details=model.coverage_details,
            valid_from=model.valid_from,
            valid_until=model.valid_until,
            status=model.status.code if model.status else None,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def save(self, insurance_policy: InsurancePolicy, status_id: UUID) -> InsurancePolicy:
        """Save a new insurance policy with catalog ID"""
        model = InsurancePolicyModel(
            id=insurance_policy.id,
            patient_id=insurance_policy.patient_id,
            provider_id=insurance_policy.provider_id,
            policy_number=insurance_policy.policy_number,
            coverage_details=insurance_policy.coverage_details,
            valid_from=insurance_policy.valid_from,
            valid_until=insurance_policy.valid_until,
            status_id=status_id,
            created_at=insurance_policy.created_at,
            updated_at=insurance_policy.updated_at
        )
        self.session.add(model)
        await self.session.commit()

        # Refresh with relationships loaded
        await self.session.refresh(model, ["status", "provider"])
        return self._to_entity(model)

    async def get_by_id(self, policy_id: UUID) -> Optional[InsurancePolicy]:
        """Get insurance policy by ID"""
        result = await self.session.execute(
            select(InsurancePolicyModel)
            .options(
                selectinload(InsurancePolicyModel.status),
                selectinload(InsurancePolicyModel.provider)
            )
            .where(InsurancePolicyModel.id == policy_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_patient_id(self, patient_id: UUID) -> List[InsurancePolicy]:
        """Get all insurance policies for a patient"""
        result = await self.session.execute(
            select(InsurancePolicyModel)
            .options(
                selectinload(InsurancePolicyModel.status),
                selectinload(InsurancePolicyModel.provider)
            )
            .where(InsurancePolicyModel.patient_id == patient_id)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_active_by_patient_id(self, patient_id: UUID) -> List[InsurancePolicy]:
        """Get all active insurance policies for a patient"""
        from infrastructure.database.models import InsuranceStatusModel

        result = await self.session.execute(
            select(InsurancePolicyModel)
            .join(InsuranceStatusModel, InsurancePolicyModel.status_id == InsuranceStatusModel.id)
            .options(
                selectinload(InsurancePolicyModel.status),
                selectinload(InsurancePolicyModel.provider)
            )
            .where(
                InsurancePolicyModel.patient_id == patient_id,
                InsuranceStatusModel.code == 'ACTIVE'
            )
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, insurance_policy: InsurancePolicy, status_id: UUID) -> InsurancePolicy:
        """Update an existing insurance policy with catalog ID"""
        result = await self.session.execute(
            select(InsurancePolicyModel)
            .options(
                selectinload(InsurancePolicyModel.status),
                selectinload(InsurancePolicyModel.provider)
            )
            .where(InsurancePolicyModel.id == insurance_policy.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.provider_id = insurance_policy.provider_id
            model.coverage_details = insurance_policy.coverage_details
            model.valid_from = insurance_policy.valid_from
            model.valid_until = insurance_policy.valid_until
            model.status_id = status_id
            model.updated_at = insurance_policy.updated_at

            await self.session.commit()
            await self.session.refresh(model, ["status", "provider"])
            return self._to_entity(model)

        return insurance_policy

    async def delete(self, policy_id: UUID) -> bool:
        """Delete an insurance policy"""
        result = await self.session.execute(
            select(InsurancePolicyModel).where(InsurancePolicyModel.id == policy_id)
        )
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.commit()
            return True

        return False

    async def exists_by_policy_number(self, policy_number: str) -> bool:
        """Check if insurance policy exists by policy number"""
        result = await self.session.execute(
            select(InsurancePolicyModel).where(
                InsurancePolicyModel.policy_number == policy_number
            )
        )
        return result.scalar_one_or_none() is not None
