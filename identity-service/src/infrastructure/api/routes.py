"""API routes - FastAPI endpoints"""
from typing import List, Optional

from application.dto.role_request import AssignRoleRequest, RemoveRoleRequest
from application.dto.role_response import (RoleAssignmentResponse,
                                           RoleListResponse, RoleResponse,
                                           UserRolesResponse)
from application.dto.user_request import (CreateUserRequest, LoginRequest,
                                          RefreshTokenRequest,
                                          ValidateTokenRequest)
from application.dto.user_response import (ErrorResponse, TokenResponse,
                                           TokenValidationResponse,
                                           UserResponse)
from application.use_cases.assign_role_to_user import (
    AssignRoleToUserUseCase, RoleAlreadyAssignedError)
from application.use_cases.assign_role_to_user import \
    RoleNotFoundError as AssignRoleNotFoundError
from application.use_cases.assign_role_to_user import \
    UserNotFoundError as AssignUserNotFoundError
from application.use_cases.create_user import (CreateUserUseCase,
                                               DuplicateUserError,
                                               UnauthorizedError,
                                               ValidationError)
from application.use_cases.delete_user import DeleteUserUseCase
from application.use_cases.delete_user import \
    UserNotFoundError as DeleteUserNotFoundError
from application.use_cases.get_current_user import GetCurrentUserUseCase
from application.use_cases.get_current_user import \
    UserNotFoundError as GetUserNotFoundError
from application.use_cases.get_user_by_national_id import \
    GetUserByNationalIdUseCase
from application.use_cases.get_user_roles import GetUserRolesUseCase
from application.use_cases.get_user_roles import \
    UserNotFoundError as GetRolesUserNotFoundError
from application.use_cases.list_roles import ListRolesUseCase
from application.use_cases.list_users import ListUsersUseCase
from application.use_cases.login_user import LoginUserUseCase
from application.use_cases.logout_user import LogoutUserUseCase
from application.use_cases.remove_role_from_user import (
    RemoveRoleFromUserUseCase, RoleNotAssignedError)
from application.use_cases.remove_role_from_user import \
    RoleNotFoundError as RemoveRoleNotFoundError
from application.use_cases.remove_role_from_user import \
    UserNotFoundError as RemoveUserNotFoundError
from application.use_cases.update_user import \
    UnauthorizedError as UpdateUnauthorizedError
from application.use_cases.update_user import UpdateUserUseCase
from application.use_cases.update_user import \
    UserNotFoundError as UpdateUserNotFoundError
from application.use_cases.validate_token import ValidateTokenUseCase
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from infrastructure.api.dependencies import (
    get_assign_role_to_user_use_case, get_create_user_use_case,
    get_current_rrhh_user, get_current_user, get_current_user_use_case,
    get_delete_user_use_case, get_jwt_handler, get_list_roles_use_case,
    get_list_users_use_case, get_login_user_use_case, get_logout_user_use_case,
    get_remove_role_from_user_use_case, get_role_repository,
    get_update_user_use_case, get_user_by_national_id_use_case,
    get_user_repository, get_user_roles_use_case, get_validate_token_use_case,
    security)
from infrastructure.database.repositories.user_repository_impl import \
    UserRepositoryImpl
from infrastructure.security.jwt_handler import JWTHandler

# API version 1 router
router = APIRouter(prefix="/api/v1", tags=["identity-service"])


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def _build_user_response_with_roles(user, role_repository) -> UserResponse:
    """
    Helper function to build UserResponse with roles from database

    Args:
        user: User entity from domain
        role_repository: Role repository instance

    Returns:
        UserResponse with roles populated from database
    """
    # Get user roles from database
    user_roles = await role_repository.get_user_roles(user.id)

    # Determine primary role
    if user.is_superuser:
        primary_role = "RRHH"
    elif user_roles:
        active_roles = [r for r in user_roles if r.is_active]
        primary_role = active_roles[0].code if active_roles else "USER"
    else:
        primary_role = "USER"

    # Get all role codes
    role_codes = [role.code for role in user_roles if role.is_active]
    if user.is_superuser and "RRHH" not in role_codes:
        role_codes.append("RRHH")
    if not role_codes:
        role_codes.append("USER")

    return UserResponse(
        id=user.id,
        national_id_number=user.national_id_number,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        birth_date=user.birth_date,
        address=user.address,
        role=primary_role,
        roles=role_codes,
        username=user.username,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login
    )


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Validation error"},
        403: {"model": ErrorResponse, "description": "Forbidden - RRHH role required"},
        409: {"model": ErrorResponse, "description": "Conflict - User already exists"}
    },
    summary="Register a new user",
    description="Create a new user account. Only users with RRHH role can create new users."
)
async def register(
    request: CreateUserRequest,
    current_user: dict = Depends(get_current_rrhh_user),
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> UserResponse:
    """
    Register a new user (RRHH only)

    - **national_id_number**: National ID number (6-10 digits)
    - **full_name**: User's full name
    - **email**: Valid email address
    - **phone**: Phone number (1-10 digits)
    - **birth_date**: Date of birth (max 150 years old)
    - **address**: Address (max 30 chars)
    - **role**: User role (RRHH, ADMIN, SOPORTE, ENFERMERA, MEDICO)
    - **username**: Unique username (alphanumeric, max 15 chars)
    - **password**: Strong password (min 8 chars, 1 uppercase, 1 number, 1 special char)
    """
    try:
        return await use_case.execute(request, current_user_role=current_user.get("role"))
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except DuplicateUserError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid credentials"},
        400: {"model": ErrorResponse, "description": "Bad Request"}
    },
    summary="User login",
    description="Authenticate user with email/username and password, returns access and refresh tokens"
)
async def login(
    request: LoginRequest,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case)
) -> TokenResponse:
    """
    Authenticate user and return tokens

    - **identifier**: Email or username
    - **password**: User's password
    """
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/auth/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid refresh token"},
        400: {"model": ErrorResponse, "description": "Bad Request"}
    },
    summary="Refresh access token",
    description="Get a new access token using a valid refresh token"
)
async def refresh_token(
    request: RefreshTokenRequest,
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    role_repository = Depends(get_role_repository)
) -> TokenResponse:
    """
    Refresh access token

    - **refresh_token**: Valid refresh token
    """
    try:
        # Verify refresh token
        payload = jwt_handler.verify_token(request.refresh_token, token_type="refresh")

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        # Get user from database
        user_id = payload.get("sub")
        user = await user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )

        # Get user roles from database
        user_roles = await role_repository.get_user_roles(user.id)

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

        # Generate new tokens
        access_token = jwt_handler.create_access_token(
            user_id=str(user.id),
            username=user.username,
            email=user.email,
            is_superuser=user.is_superuser,
            role=primary_role,
            roles=role_codes
        )

        new_refresh_token = jwt_handler.create_refresh_token(
            user_id=str(user.id)
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=jwt_handler.access_token_expire_minutes * 60,
            user=UserResponse(
                id=user.id,
                national_id_number=user.national_id_number,
                full_name=user.full_name,
                email=user.email,
                phone=user.phone,
                birth_date=user.birth_date,
                address=user.address,
                role=primary_role,
                roles=role_codes,
                username=user.username,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at,
                last_login=user.last_login
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/auth/logout",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"}
    },
    summary="User logout",
    description="Logout current user and invalidate the access token"
)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: dict = Depends(get_current_user),
    use_case: LogoutUserUseCase = Depends(get_logout_user_use_case)
) -> dict:
    """
    Logout current user and blacklist the token

    This endpoint:
    1. Adds the current access token to the blacklist
    2. Invalidates the token server-side
    3. Client should also discard both access and refresh tokens

    Note: The refresh token should also be discarded by the client.
    For additional security, also blacklist the refresh token if provided.

    Returns:
        Success message with user ID
    """
    try:
        token = credentials.credentials
        user_id = current_user.get("sub")
        return await use_case.execute(access_token=token, user_id=user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/auth/validate",
    response_model=TokenValidationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"}
    },
    summary="Validate JWT token",
    description="Validate a JWT access token and return user information"
)
async def validate_token(
    request: ValidateTokenRequest,
    use_case: ValidateTokenUseCase = Depends(get_validate_token_use_case)
) -> TokenValidationResponse:
    """
    Validate a JWT token

    - **token**: JWT access token to validate
    """
    try:
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@router.get(
    "/users/{national_id_number}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not Found - User not found"}
    },
    summary="Get user by national_id_number",
    description="Retrieve a user's information by their national_id_number (national ID)"
)
async def get_user_by_national_id_number(
    national_id_number: str,
    _: dict = Depends(get_current_user),
    use_case: GetUserByNationalIdUseCase = Depends(get_user_by_national_id_use_case),
    role_repository = Depends(get_role_repository)
) -> UserResponse:
    
    try:
        user = await use_case.execute(national_id_number)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with national_id_number {national_id_number} not found"
            )

        return await _build_user_response_with_roles(user, role_repository)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.put(
    "/users/{national_id_number}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not Found - User not found"},
        400: {"model": ErrorResponse, "description": "Bad Request - Validation error"}
    },
    summary="Update user",
    description="Update user information (authenticated users can update their own data)"
)
async def update_user(
    national_id_number: str,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
    role_repository = Depends(get_role_repository)
) -> UserResponse:
    """
    Update user information

    - **national_id_number**: User's national ID number
    - **full_name**: New full name (optional)
    - **email**: New email (optional)
    - **phone**: New phone (optional)
    - **address**: New address (optional)
    """
    try:
        current_user_national_id = current_user.get("national_id_number")
        current_user_role = current_user.get("role")

        updated_user = await use_case.execute(
            national_id_number=national_id_number,
            current_user_national_id=current_user_national_id,
            current_user_role=current_user_role,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address
        )

        return await _build_user_response_with_roles(updated_user, role_repository)

    except HTTPException:
        raise
    except UpdateUnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except UpdateUserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.delete(
    "/users/{national_id_number}",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden - RRHH role required"},
        404: {"model": ErrorResponse, "description": "Not Found - User not found"}
    },
    summary="Delete user",
    description="Delete a user (RRHH only)"
)
async def delete_user(
    national_id_number: str,
    _: dict = Depends(get_current_rrhh_user),
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case)
) -> dict:
    """
    Delete user (RRHH only)

    - **national_id_number**: User's national ID number to delete
    """
    try:
        await use_case.execute(national_id_number)

        return {
            "message": f"User with national_id_number {national_id_number} successfully deleted",
            "deleted_national_id_number": national_id_number
        }

    except HTTPException:
        raise
    except DeleteUserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/users",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden - RRHH role required"}
    },
    summary="List all users",
    description="Get a list of all users (RRHH only)"
)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    _: dict = Depends(get_current_rrhh_user),
    use_case: ListUsersUseCase = Depends(get_list_users_use_case),
    role_repository = Depends(get_role_repository)
) -> List[UserResponse]:
    """
    List all users (RRHH only)

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        users = await use_case.execute(skip=skip, limit=limit)

        # Build user responses with roles from database
        user_responses = []
        for user in users:
            user_response = await _build_user_response_with_roles(user, role_repository)
            user_responses.append(user_response)

        return user_responses

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# CURRENT USER ENDPOINT
# ============================================================================

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"}
    },
    summary="Get current user",
    description="Get information about the currently authenticated user"
)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    use_case: GetCurrentUserUseCase = Depends(get_current_user_use_case),
    role_repository = Depends(get_role_repository)
) -> UserResponse:
    """Get current authenticated user information"""
    try:
        user_id = current_user.get("sub")
        user = await use_case.execute(user_id)

        return await _build_user_response_with_roles(user, role_repository)

    except HTTPException:
        raise
    except GetUserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# ROLE MANAGEMENT ENDPOINTS
# ============================================================================

@router.get(
    "/roles",
    response_model=RoleListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden - RRHH role required"}
    },
    summary="List all roles",
    description="Get a list of all available roles (RRHH only)"
)
async def list_roles(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    only_active: bool = Query(True, description="Filter only active roles"),
    _: dict = Depends(get_current_rrhh_user),
    use_case: ListRolesUseCase = Depends(get_list_roles_use_case)
) -> RoleListResponse:
    """
    List all roles (RRHH only)

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **only_active**: If true, return only active roles
    """
    try:
        roles = await use_case.execute(skip=skip, limit=limit, only_active=only_active)

        role_responses = [
            RoleResponse(
                id=role.id,
                code=role.code,
                name=role.name,
                description=role.description,
                is_active=role.is_active,
                created_at=role.created_at,
                updated_at=role.updated_at
            )
            for role in roles
        ]

        return RoleListResponse(
            roles=role_responses,
            total=len(role_responses),
            skip=skip,
            limit=limit
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/users/{user_id}/roles",
    response_model=UserRolesResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden - RRHH role required"},
        404: {"model": ErrorResponse, "description": "Not Found - User not found"}
    },
    summary="Get user's roles",
    description="Get all roles assigned to a specific user (RRHH only)"
)
async def get_user_roles(
    user_id: str,
    _: dict = Depends(get_current_rrhh_user),
    use_case: GetUserRolesUseCase = Depends(get_user_roles_use_case)
) -> UserRolesResponse:
    """
    Get all roles assigned to a user (RRHH only)

    - **user_id**: UUID of the user
    """
    try:
        from uuid import UUID
        user_uuid = UUID(user_id)
        roles = await use_case.execute(user_uuid)

        role_responses = [
            RoleResponse(
                id=role.id,
                code=role.code,
                name=role.name,
                description=role.description,
                is_active=role.is_active,
                created_at=role.created_at,
                updated_at=role.updated_at
            )
            for role in roles
        ]

        return UserRolesResponse(
            user_id=user_uuid,
            roles=role_responses
        )

    except HTTPException:
        raise
    except GetRolesUserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/users/roles/assign",
    response_model=RoleAssignmentResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden - RRHH role required"},
        404: {"model": ErrorResponse, "description": "Not Found - User or Role not found"},
        409: {"model": ErrorResponse, "description": "Conflict - Role already assigned"}
    },
    summary="Assign role to user",
    description="Assign a role to a user (RRHH only)"
)
async def assign_role_to_user(
    request: AssignRoleRequest,
    _: dict = Depends(get_current_rrhh_user),
    use_case: AssignRoleToUserUseCase = Depends(get_assign_role_to_user_use_case)
) -> RoleAssignmentResponse:
    """
    Assign a role to a user (RRHH only)

    - **user_id**: UUID of the user
    - **role_id**: UUID of the role to assign
    """
    try:
        await use_case.execute(request.user_id, request.role_id)

        return RoleAssignmentResponse(
            success=True,
            message="Role assigned successfully",
            user_id=request.user_id,
            role_id=request.role_id
        )

    except HTTPException:
        raise
    except AssignUserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except AssignRoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RoleAlreadyAssignedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/users/roles/remove",
    response_model=RoleAssignmentResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden - RRHH role required"},
        404: {"model": ErrorResponse, "description": "Not Found - User or Role not found"},
        409: {"model": ErrorResponse, "description": "Conflict - Role not assigned to user"}
    },
    summary="Remove role from user",
    description="Remove a role from a user (RRHH only)"
)
async def remove_role_from_user(
    request: RemoveRoleRequest,
    _: dict = Depends(get_current_rrhh_user),
    use_case: RemoveRoleFromUserUseCase = Depends(get_remove_role_from_user_use_case)
) -> RoleAssignmentResponse:
    """
    Remove a role from a user (RRHH only)

    - **user_id**: UUID of the user
    - **role_id**: UUID of the role to remove
    """
    try:
        await use_case.execute(request.user_id, request.role_id)

        return RoleAssignmentResponse(
            success=True,
            message="Role removed successfully",
            user_id=request.user_id,
            role_id=request.role_id
        )

    except HTTPException:
        raise
    except RemoveUserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RemoveRoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RoleNotAssignedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the identity service is running and healthy"
)
async def health_check() -> dict:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "identity-service",
        "version": "1.0.0"
    }