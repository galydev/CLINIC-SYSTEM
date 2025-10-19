"""Create user use case - Application layer business logic"""
import bcrypt
from typing import Optional
import logging

from application.dto.user_request import CreateUserRequest, UserRole
from application.dto.user_response import UserResponse
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.repositories.role_repository import RoleRepository

logger = logging.getLogger(__name__)


class UnauthorizedError(Exception):
    """Exception raised when user is not authorized to perform an action"""
    pass


class DuplicateUserError(Exception):
    """Exception raised when trying to create a user that already exists"""
    pass


class ValidationError(Exception):
    """Exception raised when user data validation fails"""
    pass


class CreateUserUseCase:
    """
    Use case for creating a new user

    Only users with RRHH role can execute this use case.
    Validates all user data including national_id_number uniqueness, username uniqueness,
    email format, password strength, and birth date (max 150 years).
    Assigns the specified role to the user from the database.
    """

    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def execute(
        self,
        request: CreateUserRequest,
        current_user_role: Optional[str] = None
    ) -> UserResponse:
        """
        Execute the create user use case

        Args:
            request: CreateUserRequest with user data
            current_user_role: Role of the user executing this use case

        Returns:
            UserResponse with created user data (without password)

        Raises:
            UnauthorizedError: If current user doesn't have RRHH role
            DuplicateUserError: If national_id_number or username already exists
            ValidationError: If any validation fails
        """
        # Authorization check - only RRHH can create users
        if current_user_role != UserRole.RRHH.value:
            raise UnauthorizedError(
                "Only users with RRHH role can create new users"
            )

        # Validate password strength (min 8 chars, 1 uppercase, 1 number, 1 special)
        self._validate_password(request.password)

        # Check national_id_number uniqueness
        existing_user_by_national_id = await self.user_repository.get_by_national_id_number(
            request.national_id_number
        )
        if existing_user_by_national_id:
            raise DuplicateUserError(
                f"User with national ID number {request.national_id_number} already exists"
            )

        # Check username uniqueness
        existing_user_by_username = await self.user_repository.get_by_username(
            request.username
        )
        if existing_user_by_username:
            raise DuplicateUserError(
                f"Username {request.username} is already taken"
            )

        # Check email uniqueness (case-insensitive)
        existing_user_by_email = await self.user_repository.get_by_email(
            request.email.lower()
        )
        if existing_user_by_email:
            raise DuplicateUserError(
                f"Email {request.email} is already registered"
            )

        # Hash password with bcrypt
        hashed_password = self._hash_password(request.password)

        # Create user entity
        # Note: User.create already validates national_id_number, email, phone, birth_date, address, username
        user = User.create(
            national_id_number=request.national_id_number,
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            birth_date=request.birth_date,
            address=request.address,
            username=request.username,
            hashed_password=hashed_password,
            role_ids=[],  # We'll use the role field from the model instead
            is_superuser=False
        )

        # Persist user
        created_user = await self.user_repository.save(user)

        # Find role in database by code
        role_code = request.role.value
        logger.info(f"Looking for role with code: {role_code}")
        role = await self.role_repository.get_by_code(role_code)

        if not role:
            logger.warning(f"Role '{role_code}' not found in database, user created without role")
            # User created but role not found - could assign default USER role or raise error
            # For now, we'll log a warning and continue
            role_codes = []
        else:
            # Assign role to user
            logger.info(f"Assigning role '{role.code}' to user {created_user.username}")
            await self.user_repository.assign_role(created_user.id, role.id)
            role_codes = [role.code]

        # Return response DTO (without password)
        return UserResponse(
            id=created_user.id,
            national_id_number=created_user.national_id_number,
            full_name=created_user.full_name,
            email=created_user.email,
            phone=created_user.phone,
            birth_date=created_user.birth_date,
            address=created_user.address,
            role=role_code,  # Primary role from request
            roles=role_codes,  # Actual roles from database
            username=created_user.username,
            is_active=created_user.is_active,
            is_superuser=created_user.is_superuser,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
            last_login=created_user.last_login
        )

    def _validate_password(self, password: str) -> None:
        """
        Validate password strength

        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one number
        - At least one special character

        Args:
            password: Plain text password to validate

        Raises:
            ValidationError: If password doesn't meet requirements
        """
        if len(password) < 8:
            raise ValidationError(
                "Password must contain at least 8 characters"
            )

        if not any(c.isupper() for c in password):
            raise ValidationError(
                "Password must include at least one uppercase letter"
            )

        if not any(c.isdigit() for c in password):
            raise ValidationError(
                "Password must include at least one number"
            )

        # Check for special characters
        special_chars = set('!@#$%^&*(),.?":{}|<>_-+=[]\\\/;`~')
        if not any(c in special_chars for c in password):
            raise ValidationError(
                "Password must include at least one special character"
            )

    def _hash_password(self, password: str) -> str:
        """
        Hash password using bcrypt

        Args:
            password: Plain text password

        Returns:
            Hashed password as string
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
