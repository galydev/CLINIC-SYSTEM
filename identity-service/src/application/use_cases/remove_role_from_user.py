"""Remove role from user use case"""
from uuid import UUID
import logging

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.repositories.role_repository import RoleRepository

logger = logging.getLogger(__name__)


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    pass


class RoleNotFoundError(Exception):
    """Raised when role is not found"""
    pass


class RoleNotAssignedError(Exception):
    """Raised when role is not assigned to user"""
    pass


class RemoveRoleFromUserUseCase:
    """Use case for removing a role from a user"""

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def execute(self, user_id: UUID, role_id: UUID) -> User:
        """
        Remove a role from a user

        Args:
            user_id: UUID of the user
            role_id: UUID of the role to remove

        Returns:
            Updated User entity without the removed role

        Raises:
            UserNotFoundError: If user is not found
            RoleNotFoundError: If role is not found
            RoleNotAssignedError: If role is not assigned to the user
            ValueError: If user_id or role_id is invalid
        """
        if not user_id or not isinstance(user_id, UUID):
            raise ValueError("User ID must be a valid UUID")

        if not role_id or not isinstance(role_id, UUID):
            raise ValueError("Role ID must be a valid UUID")

        logger.info(f"Removing role {role_id} from user {user_id}")

        # Verify user exists
        user = await self.user_repository.get_by_id(str(user_id))
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise UserNotFoundError(f"User with ID {user_id} not found")

        # Verify role exists
        role = await self.role_repository.get_by_id(str(role_id))
        if not role:
            logger.warning(f"Role not found: {role_id}")
            raise RoleNotFoundError(f"Role with ID {role_id} not found")

        # Remove role
        try:
            updated_user = await self.user_repository.remove_role(user_id, role_id)
            logger.info(f"Successfully removed role {role.code} from user {user.username}")
            return updated_user
        except ValueError as e:
            # Handle case where role is not assigned
            if "not assigned" in str(e).lower():
                logger.warning(f"Role {role.code} not assigned to user {user.username}")
                raise RoleNotAssignedError(str(e))
            raise
