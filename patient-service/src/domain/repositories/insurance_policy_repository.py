"""Insurance Policy repository interface - Domain layer contract"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.insurance_policy import InsurancePolicy


class InsurancePolicyRepository(ABC):

    @abstractmethod
    async def save(self, insurance_policy: InsurancePolicy) -> InsurancePolicy:
        pass

    @abstractmethod
    async def get_by_id(self, policy_id: UUID) -> Optional[InsurancePolicy]:
        pass

    @abstractmethod
    async def get_by_patient_id(self, patient_id: UUID) -> List[InsurancePolicy]:
        pass

    @abstractmethod
    async def get_active_by_patient_id(self, patient_id: UUID) -> List[InsurancePolicy]:
        pass

    @abstractmethod
    async def update(self, insurance_policy: InsurancePolicy) -> InsurancePolicy:
        pass

    @abstractmethod
    async def delete(self, policy_id: UUID) -> bool:
        pass

    @abstractmethod
    async def exists_by_policy_number(self, policy_number: str) -> bool:
        pass
