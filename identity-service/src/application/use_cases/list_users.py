"""List users use case"""
from typing import List

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class ListUsersUseCase:
    """Use case for listing all users with pagination (RRHH only)"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        List all users with pagination

        Args:
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)

        Returns:
            List of user entities

        Raises:
            ValueError: If pagination parameters are invalid
        """
        if skip < 0:
            raise ValueError("Skip parameter must be non-negative")

        if limit < 1 or limit > 1000:
            raise ValueError("Limit parameter must be between 1 and 1000")

        return await self.user_repository.get_all(skip=skip, limit=limit)
