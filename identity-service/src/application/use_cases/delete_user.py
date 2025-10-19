"""Delete user use case"""
from domain.repositories.user_repository import UserRepository


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    pass


class DeleteUserUseCase:
    """Use case for deleting a user (RRHH only)"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, national_id_number: str) -> bool:
        """
        Delete a user by national ID number

        Args:
            national_id_number: National ID of user to delete

        Returns:
            True if user was deleted successfully

        Raises:
            UserNotFoundError: If user is not found
            ValueError: If national_id_number is invalid
        """
        if not national_id_number or not isinstance(national_id_number, str):
            raise ValueError("National ID number must be a non-empty string")

        # Check if user exists
        user = await self.user_repository.get_by_national_id_number(national_id_number)
        if not user:
            raise UserNotFoundError(f"User with national ID {national_id_number} not found")

        # Delete user
        deleted = await self.user_repository.delete(national_id_number)

        if not deleted:
            raise Exception("Failed to delete user")

        return True
