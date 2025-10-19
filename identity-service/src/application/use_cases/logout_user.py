"""Logout user use case"""
from infrastructure.security.token_blacklist import TokenBlacklist


class LogoutUserUseCase:
    """Use case for logging out a user by blacklisting their token"""

    def __init__(self, token_blacklist: TokenBlacklist):
        self.token_blacklist = token_blacklist

    async def execute(self, access_token: str, user_id: str) -> dict:
        """
        Logout user by adding their access token to the blacklist

        Args:
            access_token: JWT access token to invalidate
            user_id: ID of the user logging out

        Returns:
            Dictionary with logout confirmation

        Raises:
            ValueError: If token or user_id is invalid
        """
        if not access_token or not isinstance(access_token, str):
            raise ValueError("Access token must be a non-empty string")

        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")

        # Add token to blacklist
        self.token_blacklist.add_token(access_token)

        return {
            "message": "Successfully logged out",
            "user_id": user_id,
            "detail": "Token has been invalidated. Please discard your tokens."
        }
