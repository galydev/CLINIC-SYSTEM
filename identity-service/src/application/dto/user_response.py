"""User response DTOs - Data Transfer Objects for outgoing responses"""
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    """DTO for user data response"""
    id: UUID
    national_id_number: str
    full_name: str
    email: EmailStr
    phone: str
    birth_date: date
    address: str
    role: str  # Primary role for backward compatibility
    roles: Optional[List[str]] = None  # All user roles
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "national_id_number": "1234567890",
                "full_name": "John Doe",
                "email": "user@example.com",
                "phone": "3001234567",
                "birth_date": "1990-01-01",
                "address": "Calle 123 #45-67",
                "role": "MEDICO",
                "username": "john_doe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
                "last_login": "2025-01-01T12:00:00"
            }
        }


class TokenResponse(BaseModel):
    """DTO for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "username": "john_doe",
                    "full_name": "John Doe",
                    "is_active": True,
                    "is_superuser": False,
                    "created_at": "2025-01-01T00:00:00",
                    "updated_at": "2025-01-01T00:00:00",
                    "last_login": "2025-01-01T12:00:00"
                }
            }
        }


class TokenValidationResponse(BaseModel):
    """DTO for token validation response"""
    valid: bool
    user_id: Optional[UUID] = None
    username: Optional[str] = None
    email: Optional[str] = None
    is_superuser: bool = False
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "john_doe",
                "email": "user@example.com",
                "is_superuser": False,
                "message": "Token is valid"
            }
        }


class ErrorResponse(BaseModel):
    """DTO for error responses"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Authentication failed",
                "detail": "Invalid credentials",
                "code": "AUTH_001"
            }
        }
