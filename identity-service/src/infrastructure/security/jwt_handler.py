"""JWT handler - Token generation and validation"""
from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import JWTError, jwt


class JWTHandler:
    """Handler for JWT token operations"""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(
        self,
        user_id: str,
        username: str,
        email: str,
        is_superuser: bool = False,
        role: str = "USER",
        roles: list = None
    ) -> str:
        """
        Create a new access token

        Args:
            user_id: User ID
            username: Username
            email: User email
            is_superuser: Whether user is superuser
            role: Primary user role (RRHH, ADMIN, SOPORTE, ENFERMERA, MEDICO, USER)
            roles: List of all user role codes

        Returns:
            Encoded JWT access token
        """
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": user_id,
            "username": username,
            "email": email,
            "is_superuser": is_superuser,
            "role": role,  # Primary role for backward compatibility
            "roles": roles or [role],  # All user roles
            "type": "access",
            "exp": expire,
            "iat": datetime.utcnow()
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """
        Create a new refresh token

        Args:
            user_id: User ID

        Returns:
            Encoded JWT refresh token
        """
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)

        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expire,
            "iat": datetime.utcnow()
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[Dict]:
        """
        Decode and validate a JWT token

        Args:
            token: JWT token to decode

        Returns:
            Decoded payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError:
            return None

    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict]:
        """
        Verify a JWT token and check its type

        Args:
            token: JWT token to verify
            token_type: Expected token type (access or refresh)

        Returns:
            Decoded payload if valid and type matches, None otherwise
        """
        payload = self.decode_token(token)

        if not payload:
            return None

        if payload.get("type") != token_type:
            return None

        return payload

    def get_token_expiration(self, token: str) -> Optional[datetime]:
        """
        Get the expiration time of a token

        Args:
            token: JWT token

        Returns:
            Expiration datetime or None if invalid
        """
        payload = self.decode_token(token)

        if not payload:
            return None

        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            return None

        return datetime.fromtimestamp(exp_timestamp)

    def is_token_expired(self, token: str) -> bool:
        """
        Check if a token is expired

        Args:
            token: JWT token

        Returns:
            True if expired, False otherwise
        """
        expiration = self.get_token_expiration(token)

        if not expiration:
            return True

        return datetime.utcnow() > expiration
