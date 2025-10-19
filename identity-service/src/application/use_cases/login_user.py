"""Login user use case - Application layer business logic"""
from passlib.context import CryptContext

from application.dto.user_request import LoginRequest
from application.dto.user_response import TokenResponse, UserResponse
from domain.repositories.role_repository import RoleRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.security.jwt_handler import JWTHandler


class LoginUserUseCase:
    """Use case for user authentication and login"""

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        password_context: CryptContext,
        jwt_handler: JWTHandler
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.password_context = password_context
        self.jwt_handler = jwt_handler

    async def execute(self, request: LoginRequest) -> TokenResponse:
        """
        Execute the login user use case

        Args:
            request: LoginRequest with credentials

        Returns:
            TokenResponse with access token and user data

        Raises:
            ValueError: If authentication fails
        """
        # Find user by email or username
        user = await self.user_repository.get_by_email(request.identifier)
        if not user:
            user = await self.user_repository.get_by_username(request.identifier)

        # Validate user exists
        if not user:
            raise ValueError("Invalid credentials")

        # Validate user is active
        if not user.is_active:
            raise ValueError("Account is inactive")

        # Verify password
        if not self.password_context.verify(request.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        # Update last login timestamp
        user.update_last_login()
        await self.user_repository.update(user)

        # Get user roles from database
        user_roles = await self.role_repository.get_user_roles(user.id)

        # Determine primary role and role codes
        if user.is_superuser:
            # Superuser always has RRHH as primary role
            primary_role = "RRHH"
        elif user_roles:
            # Use the first active role as primary
            active_roles = [r for r in user_roles if r.is_active]
            primary_role = active_roles[0].code if active_roles else "USER"
        else:
            # Fallback to USER if no roles assigned
            primary_role = "USER"

        # Get all role codes for JWT
        role_codes = [role.code for role in user_roles if role.is_active]

        # If no roles but superuser, add RRHH
        if user.is_superuser and "RRHH" not in role_codes:
            role_codes.append("RRHH")

        # If no roles at all, add USER as fallback
        if not role_codes:
            role_codes.append("USER")

        # Generate JWT tokens
        access_token = self.jwt_handler.create_access_token(
            user_id=str(user.id),
            username=user.username,
            email=user.email,
            is_superuser=user.is_superuser,
            role=primary_role,
            roles=role_codes
        )

        refresh_token = self.jwt_handler.create_refresh_token(
            user_id=str(user.id)
        )

        # Create user response
        user_response = UserResponse(
            id=user.id,
            national_id_number=user.national_id_number,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            birth_date=user.birth_date,
            address=user.address,
            role=primary_role,
            username=user.username,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )

        # Return token response
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=self.jwt_handler.access_token_expire_minutes * 60,
            user=user_response
        )
