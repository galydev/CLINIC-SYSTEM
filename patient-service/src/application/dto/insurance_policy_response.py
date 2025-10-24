from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class InsurancePolicyResponse(BaseModel):
    id: UUID
    patient_id: UUID
    provider_id: UUID
    policy_number: str
    coverage_details: str
    valid_from: date
    valid_until: date
    status: str = Field(..., description="Insurance status code (e.g., 'ACTIVE', 'INACTIVE', 'SUSPENDED', 'EXPIRED')")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "provider_id": "123e4567-e89b-12d3-a456-426614174003",
                "policy_number": "POL-2024-12345",
                "coverage_details": "Full medical coverage",
                "valid_from": "2024-01-01",
                "valid_until": "2025-12-31",
                "status": "ACTIVE",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class InsuranceStatusResponse(BaseModel):

    patient_id: UUID
    has_active_insurance: bool
    active_policy: InsurancePolicyResponse | None
    has_policy: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "has_active_insurance": True,
                "active_policy": {
                    "id": "123e4567-e89b-12d3-a456-426614174002",
                    "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                    "provider_id": "123e4567-e89b-12d3-a456-426614174003",
                    "policy_number": "POL-2024-12345",
                    "coverage_details": "Full medical coverage",
                    "valid_from": "2024-01-01",
                    "valid_until": "2025-12-31",
                    "status": "ACTIVE",
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                "has_policy": True
            }
        }
