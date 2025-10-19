"""List roles use case"""
from typing import List
import logging

from domain.entities.role import Role
from domain.repositories.role_repository import RoleRepository

logger = logging.getLogger(__name__)


class ListRolesUseCase:
    """Use case for listing all roles with pagination"""

    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True
    ) -> List[Role]:
        """
        Get all roles with pagination

        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            only_active: If True, return only active roles

        Returns:
            List of Role entities

        Raises:
            ValueError: If pagination parameters are invalid
        """
        if skip < 0:
            raise ValueError("Skip must be non-negative")

        if limit < 1 or limit > 1000:
            raise ValueError("Limit must be between 1 and 1000")

        logger.info(f"Listing roles with skip={skip}, limit={limit}, only_active={only_active}")

        roles = await self.role_repository.get_all(
            skip=skip,
            limit=limit,
            only_active=only_active
        )

        logger.info(f"Retrieved {len(roles)} roles")
        return roles
