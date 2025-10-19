"""User request DTOs - Data Transfer Objects for incoming requests"""
from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, validator
import re


class UserRole(str, Enum):
    """User role enumeration"""
    RRHH = "RRHH"
    ADMIN = "ADMIN"
    SOPORTE = "SOPORTE"
    ENFERMERA = "ENFERMERA"
    MEDICO = "MEDICO"


class CreateUserRequest(BaseModel):
    """DTO for creating a new user"""
    national_id_number: str = Field(..., min_length=6, max_length=10, description="National ID number")
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=10, description="Phone number")
    birth_date: date = Field(..., description="Date of birth")
    address: str = Field(..., min_length=1, max_length=30)
    role: UserRole = Field(..., description="User role")
    username: str = Field(..., min_length=1, max_length=15)
    password: str = Field(..., min_length=8, max_length=128)

    @validator("national_id_number")
    def validate_national_id_number(cls, v):
        """Validate national ID number format - must be numeric"""
        if not v.isdigit():
            raise ValueError("National ID number must contain only digits")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        """Validate phone format - must be numeric"""
        if not v.isdigit():
            raise ValueError("Phone must contain only digits")
        return v

    @validator("username")
    def validate_username(cls, v):
        """Validate username format - alphanumeric only"""
        if not re.match(r"^[a-zA-Z0-9]+$", v):
            raise ValueError("Username must contain only letters and numbers")
        return v

    @validator("birth_date")
    def validate_birth_date(cls, v):
        """Validate birth date - max 150 years old"""
        from datetime import date as date_type
        today = date_type.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))

        if v > today:
            raise ValueError("Birth date cannot be in the future")
        if age > 150:
            raise ValueError("Age cannot exceed 150 years")
        if age < 0:
            raise ValueError("Invalid birth date")

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "national_id_number": "1234567890",
                "full_name": "John Doe",
                "email": "user@example.com",
                "phone": "3001234567",
                "birth_date": "1990-01-01",
                "address": "Calle 123 #45-67",
                "role": "MEDICO",
                "username": "john_doe",
                "password": "SecurePass123!"
            }
        }


class LoginRequest(BaseModel):
    """DTO for user login"""
    identifier: str = Field(..., description="Email or username")
    password: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "identifier": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class ValidateTokenRequest(BaseModel):
    """DTO for token validation"""
    token: str = Field(..., description="JWT token to validate")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshTokenRequest(BaseModel):
    """DTO for token refresh"""
    refresh_token: str = Field(..., description="Refresh token")

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
