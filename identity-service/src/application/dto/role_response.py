"""Role response DTOs - Data Transfer Objects for role-related responses"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class RoleResponse(BaseModel):
    """DTO for role data response"""
    id: UUID
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "code": "MEDICO",
                "name": "Médico",
                "description": "Personal médico con acceso a funcionalidades clínicas",
                "is_active": True,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }


class RoleListResponse(BaseModel):
    """DTO for paginated list of roles"""
    roles: List[RoleResponse]
    total: int
    skip: int
    limit: int

    class Config:
        json_schema_extra = {
            "example": {
                "roles": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "code": "MEDICO",
                        "name": "Médico",
                        "description": "Personal médico con acceso a funcionalidades clínicas",
                        "is_active": True,
                        "created_at": "2025-01-01T00:00:00",
                        "updated_at": "2025-01-01T00:00:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100
            }
        }


class UserRolesResponse(BaseModel):
    """DTO for user's roles"""
    user_id: UUID
    roles: List[RoleResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "roles": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "code": "MEDICO",
                        "name": "Médico",
                        "description": "Personal médico con acceso a funcionalidades clínicas",
                        "is_active": True,
                        "created_at": "2025-01-01T00:00:00",
                        "updated_at": "2025-01-01T00:00:00"
                    }
                ]
            }
        }


class RoleAssignmentResponse(BaseModel):
    """DTO for role assignment operation response"""
    success: bool
    message: str
    user_id: UUID
    role_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Role assigned successfully",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "role_id": "123e4567-e89b-12d3-a456-426614174001"
            }
        }
