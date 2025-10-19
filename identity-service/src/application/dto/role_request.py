"""Role request DTOs - Data Transfer Objects for role-related requests"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
import re


class RoleRequest(BaseModel):
    """DTO for creating or updating a role"""
    code: str = Field(..., min_length=2, max_length=50, description="Unique role code (e.g., ADMIN, MEDICO)")
    name: str = Field(..., min_length=2, max_length=100, description="Human-readable role name")
    description: Optional[str] = Field(None, max_length=500, description="Role description")
    is_active: bool = Field(True, description="Whether the role is active")

    @validator("code")
    def validate_code(cls, v):
        """Validate role code format - uppercase alphanumeric with underscores"""
        if not re.match(r"^[A-Z0-9_]+$", v):
            raise ValueError("Role code must contain only uppercase letters, numbers, and underscores")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "code": "MEDICO",
                "name": "Médico",
                "description": "Personal médico con acceso a funcionalidades clínicas",
                "is_active": True
            }
        }


class AssignRoleRequest(BaseModel):
    """DTO for assigning a role to a user"""
    user_id: UUID = Field(..., description="ID of the user")
    role_id: UUID = Field(..., description="ID of the role to assign")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "role_id": "123e4567-e89b-12d3-a456-426614174001"
            }
        }


class RemoveRoleRequest(BaseModel):
    """DTO for removing a role from a user"""
    user_id: UUID = Field(..., description="ID of the user")
    role_id: UUID = Field(..., description="ID of the role to remove")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "role_id": "123e4567-e89b-12d3-a456-426614174001"
            }
        }
