"""Validate token use case - Application layer business logic"""
from uuid import UUID

from application.dto.user_request import ValidateTokenRequest
from application.dto.user_response import TokenValidationResponse
from infrastructure.security.jwt_handler import JWTHandler


class ValidateTokenUseCase:
    """Use case for validating JWT tokens"""

    def __init__(self, jwt_handler: JWTHandler):
        self.jwt_handler = jwt_handler

    async def execute(self, request: ValidateTokenRequest) -> TokenValidationResponse:
        """
        Execute the validate token use case

        Args:
            request: ValidateTokenRequest with token

        Returns:
            TokenValidationResponse with validation result
        """
        try:
            # Decode and validate token
            payload = self.jwt_handler.decode_token(request.token)

            if not payload:
                return TokenValidationResponse(
                    valid=False,
                    message="Invalid or expired token"
                )

            # Extract user information from payload
            user_id = payload.get("sub")
            username = payload.get("username")
            email = payload.get("email")
            is_superuser = payload.get("is_superuser", False)

            # Validate required fields
            if not user_id:
                return TokenValidationResponse(
                    valid=False,
                    message="Invalid token payload"
                )

            # Return successful validation
            return TokenValidationResponse(
                valid=True,
                user_id=UUID(user_id),
                username=username,
                email=email,
                is_superuser=is_superuser,
                message="Token is valid"
            )

        except Exception as e:
            return TokenValidationResponse(
                valid=False,
                message=f"Token validation failed: {str(e)}"
            )
