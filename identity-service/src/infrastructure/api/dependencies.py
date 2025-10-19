"""FastAPI dependencies - Dependency injection setup"""
from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.assign_role_to_user import AssignRoleToUserUseCase
from application.use_cases.create_user import CreateUserUseCase
from application.use_cases.delete_user import DeleteUserUseCase
from application.use_cases.get_current_user import GetCurrentUserUseCase
from application.use_cases.get_user_by_national_id import GetUserByNationalIdUseCase
from application.use_cases.get_user_roles import GetUserRolesUseCase
from application.use_cases.list_roles import ListRolesUseCase
from application.use_cases.list_users import ListUsersUseCase
from application.use_cases.login_user import LoginUserUseCase
from application.use_cases.logout_user import LogoutUserUseCase
from application.use_cases.remove_role_from_user import RemoveRoleFromUserUseCase
from application.use_cases.update_user import UpdateUserUseCase
from application.use_cases.validate_token import ValidateTokenUseCase
from config.database import get_db_session
from config.settings import get_settings
from infrastructure.database.repositories.role_repository_impl import RoleRepositoryImpl
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.security.jwt_handler import JWTHandler
from infrastructure.security.token_blacklist import get_token_blacklist, TokenBlacklist

# Security schemes
security = HTTPBearer()

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_context() -> CryptContext:
    """Get password hashing context"""
    return pwd_context


def get_blacklist() -> TokenBlacklist:
    """Get token blacklist instance"""
    return get_token_blacklist()


def get_jwt_handler() -> JWTHandler:
    """Get JWT handler instance"""
    settings = get_settings()
    return JWTHandler(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepositoryImpl:
    """Get user repository instance"""
    return UserRepositoryImpl(session)


async def get_role_repository(
    session: AsyncSession = Depends(get_db_session)
) -> RoleRepositoryImpl:
    """Get role repository instance"""
    return RoleRepositoryImpl(session)


async def get_create_user_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    role_repository: RoleRepositoryImpl = Depends(get_role_repository)
) -> CreateUserUseCase:
    """Get create user use case instance"""
    return CreateUserUseCase(user_repository, role_repository)


async def get_login_user_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    role_repository: RoleRepositoryImpl = Depends(get_role_repository),
    password_context: CryptContext = Depends(get_password_context),
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
) -> LoginUserUseCase:
    """Get login user use case instance"""
    return LoginUserUseCase(user_repository, role_repository, password_context, jwt_handler)


async def get_validate_token_use_case(
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
) -> ValidateTokenUseCase:
    """Get validate token use case instance"""
    return ValidateTokenUseCase(jwt_handler)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    blacklist: TokenBlacklist = Depends(get_blacklist)
) -> dict:
    """
    Get current authenticated user from JWT token

    Args:
        credentials: HTTP Bearer credentials
        jwt_handler: JWT handler instance
        blacklist: Token blacklist instance

    Returns:
        User payload from token

    Raises:
        HTTPException: If token is invalid or blacklisted
    """
    token = credentials.credentials

    # Check if token is blacklisted (logged out)
    if blacklist.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = jwt_handler.verify_token(token, token_type="access")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return payload


async def get_current_superuser(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Verify current user is a superuser

    Args:
        current_user: Current authenticated user

    Returns:
        User payload

    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.get("is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


async def get_current_rrhh_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Verify current user has RRHH role

    Args:
        current_user: Current authenticated user

    Returns:
        User payload

    Raises:
        HTTPException: If user doesn't have RRHH role
    """
    if current_user.get("role") != "RRHH":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users with RRHH role can perform this action"
        )

    return current_user


# ============================================================================
# USE CASE DEPENDENCIES
# ============================================================================

async def get_user_by_national_id_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository)
) -> GetUserByNationalIdUseCase:
    """Get user by national ID use case instance"""
    return GetUserByNationalIdUseCase(user_repository)


async def get_update_user_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository)
) -> UpdateUserUseCase:
    """Get update user use case instance"""
    return UpdateUserUseCase(user_repository)


async def get_delete_user_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository)
) -> DeleteUserUseCase:
    """Get delete user use case instance"""
    return DeleteUserUseCase(user_repository)


async def get_list_users_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository)
) -> ListUsersUseCase:
    """Get list users use case instance"""
    return ListUsersUseCase(user_repository)


async def get_current_user_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository)
) -> GetCurrentUserUseCase:
    """Get current user use case instance"""
    return GetCurrentUserUseCase(user_repository)


async def get_logout_user_use_case(
    blacklist: TokenBlacklist = Depends(get_blacklist)
) -> LogoutUserUseCase:
    """Get logout user use case instance"""
    return LogoutUserUseCase(blacklist)


# ============================================================================
# ROLE MANAGEMENT USE CASE DEPENDENCIES
# ============================================================================

async def get_assign_role_to_user_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    role_repository: RoleRepositoryImpl = Depends(get_role_repository)
) -> AssignRoleToUserUseCase:
    """Get assign role to user use case instance"""
    return AssignRoleToUserUseCase(user_repository, role_repository)


async def get_remove_role_from_user_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    role_repository: RoleRepositoryImpl = Depends(get_role_repository)
) -> RemoveRoleFromUserUseCase:
    """Get remove role from user use case instance"""
    return RemoveRoleFromUserUseCase(user_repository, role_repository)


async def get_user_roles_use_case(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    role_repository: RoleRepositoryImpl = Depends(get_role_repository)
) -> GetUserRolesUseCase:
    """Get user roles use case instance"""
    return GetUserRolesUseCase(user_repository, role_repository)


async def get_list_roles_use_case(
    role_repository: RoleRepositoryImpl = Depends(get_role_repository)
) -> ListRolesUseCase:
    """Get list roles use case instance"""
    return ListRolesUseCase(role_repository)
