"""Get current user use case"""
from typing import Optional

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    pass


class GetCurrentUserUseCase:
    """Use case for getting current authenticated user information"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> User:
        """
        Get current authenticated user by ID

        Args:
            user_id: UUID of the authenticated user

        Returns:
            User entity

        Raises:
            UserNotFoundError: If user is not found
            ValueError: If user_id is invalid
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")

        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError("User not found")

        return user
