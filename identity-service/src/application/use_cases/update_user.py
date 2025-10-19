"""Update user use case"""
from typing import Optional

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class UnauthorizedError(Exception):
    """Raised when user is not authorized to perform action"""
    pass


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    pass


class UpdateUserUseCase:
    """Use case for updating user profile information"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self,
        national_id_number: str,
        current_user_national_id: str,
        current_user_role: str,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None
    ) -> User:
        """
        Update user profile information

        Args:
            national_id_number: National ID of user to update
            current_user_national_id: National ID of user making the request
            current_user_role: Role of user making the request
            full_name: New full name (optional)
            email: New email (optional)
            phone: New phone (optional)
            address: New address (optional)

        Returns:
            Updated user entity

        Raises:
            UnauthorizedError: If user is not authorized to update this profile
            UserNotFoundError: If user to update is not found
            ValueError: If validation fails
        """
        # Authorization check: users can only update their own profile unless they're RRHH
        if current_user_national_id != national_id_number and current_user_role != "RRHH":
            raise UnauthorizedError("You can only update your own profile")

        # Get user to update
        user = await self.user_repository.get_by_national_id_number(national_id_number)
        if not user:
            raise UserNotFoundError(f"User with national ID {national_id_number} not found")

        # Update user profile using domain entity method
        try:
            user.update_profile(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address
            )
        except ValueError as e:
            raise ValueError(f"Validation error: {str(e)}")

        # Persist changes
        updated_user = await self.user_repository.update(user)

        if not updated_user:
            raise Exception("Failed to update user")

        return updated_user
