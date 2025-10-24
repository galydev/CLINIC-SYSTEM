"""Insurance Policy entity - Core domain model"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Optional
from uuid import UUID, uuid4


@dataclass
class InsurancePolicy:

    id: UUID
    patient_id: UUID
    provider_id: UUID  # Foreign key to InsuranceProvider
    policy_number: str
    coverage_details: str
    valid_from: date
    valid_until: date
    status: str  # Insurance status code (e.g., 'ACTIVE', 'INACTIVE', 'SUSPENDED', 'EXPIRED')
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        patient_id: UUID,
        provider_id: UUID,
        policy_number: str,
        coverage_details: str,
        valid_from: date,
        valid_until: date
    ) -> "InsurancePolicy":

        # Validate inputs
        InsurancePolicy._validate_policy_number(policy_number)
        InsurancePolicy._validate_coverage_details(coverage_details)
        InsurancePolicy._validate_dates(valid_from, valid_until)

        # Determine initial status based on dates
        now = datetime.utcnow().date()
        if now < valid_from:
            status = 'INACTIVE'
        elif now > valid_until:
            status = 'EXPIRED'
        else:
            status = 'ACTIVE'

        current_time = datetime.utcnow()
        return InsurancePolicy(
            id=uuid4(),
            patient_id=patient_id,
            provider_id=provider_id,
            policy_number=policy_number,
            coverage_details=coverage_details,
            valid_from=valid_from,
            valid_until=valid_until,
            status=status,
            created_at=current_time,
            updated_at=current_time
        )

    @staticmethod
    def _validate_policy_number(policy_number: str) -> None:
        if not policy_number:
            raise ValueError("Policy number cannot be empty")
        if len(policy_number) > 50:
            raise ValueError("Policy number must not exceed 50 characters")

    @staticmethod
    def _validate_coverage_details(coverage_details: str) -> None:
        if not coverage_details:
            raise ValueError("Coverage details cannot be empty")
        if len(coverage_details) > 500:
            raise ValueError("Coverage details must not exceed 500 characters")

    @staticmethod
    def _validate_dates(valid_from: date, valid_until: date) -> None:
        if valid_from >= valid_until:
            raise ValueError("Valid from date must be before valid until date")

    def update_status(self) -> None:
        now = datetime.utcnow().date()

        if self.status == 'SUSPENDED':
            # Don't auto-update if manually suspended
            return

        if now < self.valid_from:
            self.status = 'INACTIVE'
        elif now > self.valid_until:
            self.status = 'EXPIRED'
        else:
            self.status = 'ACTIVE'

        self.updated_at = datetime.utcnow()

    def suspend(self) -> None:
        self.status = 'SUSPENDED'
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        now = datetime.utcnow().date()
        if self.valid_from <= now <= self.valid_until:
            self.status = 'ACTIVE'
            self.updated_at = datetime.utcnow()
        else:
            raise ValueError("Cannot activate policy outside valid date range")

    def is_active(self) -> bool:
        return self.status == 'ACTIVE'

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "patient_id": str(self.patient_id),
            "provider_id": str(self.provider_id),
            "policy_number": self.policy_number,
            "coverage_details": self.coverage_details,
            "valid_from": self.valid_from.isoformat(),
            "valid_until": self.valid_until.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
