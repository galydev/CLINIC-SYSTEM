"""Get user roles use case"""
from uuid import UUID
from typing import List
import logging

from domain.entities.role import Role
from domain.repositories.user_repository import UserRepository
from domain.repositories.role_repository import RoleRepository

logger = logging.getLogger(__name__)


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    pass


class GetUserRolesUseCase:
    """Use case for getting all roles assigned to a user"""

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def execute(self, user_id: UUID) -> List[Role]:
        """
        Get all roles assigned to a user

        Args:
            user_id: UUID of the user

        Returns:
            List of Role entities assigned to the user

        Raises:
            UserNotFoundError: If user is not found
            ValueError: If user_id is invalid
        """
        if not user_id or not isinstance(user_id, UUID):
            raise ValueError("User ID must be a valid UUID")

        logger.info(f"Getting roles for user {user_id}")

        # Verify user exists
        user = await self.user_repository.get_by_id(str(user_id))
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise UserNotFoundError(f"User with ID {user_id} not found")

        # Get user roles
        roles = await self.role_repository.get_user_roles(user_id)
        logger.info(f"Found {len(roles)} roles for user {user.username}")

        return roles
