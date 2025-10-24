"""Insurance Provider repository interface - Domain layer contract"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from domain.entities.insurance_provider import InsuranceProvider


class InsuranceProviderRepository(ABC):
    """Abstract repository interface for InsuranceProvider entity"""

    @abstractmethod
    async def save(self, provider: InsuranceProvider) -> InsuranceProvider:
        """
        Save a new insurance provider

        Args:
            provider: InsuranceProvider entity to save

        Returns:
            Saved insurance provider entity
        """
        pass

    @abstractmethod
    async def get_by_id(self, provider_id: UUID) -> Optional[InsuranceProvider]:
        """
        Get insurance provider by ID

        Args:
            provider_id: Insurance provider UUID

        Returns:
            InsuranceProvider entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[InsuranceProvider]:
        """
        Get insurance provider by code

        Args:
            code: Provider code (e.g., 'HCP', 'MEDICARE')

        Returns:
            InsuranceProvider entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all(self, active_only: bool = True) -> List[InsuranceProvider]:
        """
        Get all insurance providers

        Args:
            active_only: If True, only return active providers

        Returns:
            List of insurance provider entities
        """
        pass

    @abstractmethod
    async def update(self, provider: InsuranceProvider) -> InsuranceProvider:
        """
        Update an existing insurance provider

        Args:
            provider: InsuranceProvider entity with updated data

        Returns:
            Updated insurance provider entity
        """
        pass

    @abstractmethod
    async def delete(self, provider_id: UUID) -> bool:
        """
        Delete an insurance provider

        Args:
            provider_id: Insurance provider UUID

        Returns:
            True if deleted successfully
        """
        pass

    @abstractmethod
    async def exists_by_code(self, code: str) -> bool:
        """
        Check if insurance provider exists by code

        Args:
            code: Provider code

        Returns:
            True if exists
        """
        pass
