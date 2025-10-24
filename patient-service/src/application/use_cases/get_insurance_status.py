"""Get insurance status use case - Application layer business logic"""
import logging
from uuid import UUID

from application.dto.insurance_policy_response import (InsurancePolicyResponse,
                                                       InsuranceStatusResponse)
from domain.repositories.insurance_policy_repository import \
    InsurancePolicyRepository
from domain.repositories.patient_repository import PatientRepository

logger = logging.getLogger(__name__)


class PatientNotFoundError(Exception):
    """Exception raised when patient is not found"""
    pass


class GetInsuranceStatusUseCase:

    def __init__(
        self,
        insurance_policy_repository: InsurancePolicyRepository,
        patient_repository: PatientRepository
    ):
        self.insurance_policy_repository = insurance_policy_repository
        self.patient_repository = patient_repository

    async def execute(self, patient_id: UUID) -> InsuranceStatusResponse:

        # Verify patient exists
        patient = await self.patient_repository.get_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(f"Patient with ID {patient_id} not found")

        # Get the patient's policy (only one allowed per patient)
        policies = await self.insurance_policy_repository.get_by_patient_id(patient_id)

        # Since only ONE policy per patient is allowed, we take the first (and only) one
        policy = policies[0] if policies else None

        # Determine if patient has an active policy
        has_active_insurance = False
        active_policy_response = None

        if policy:
            # Update status based on current dates
            policy.update_status()

            # Check if the policy is currently active
            has_active_insurance = policy.status == 'ACTIVE'

            # Only return policy details if it's active
            if has_active_insurance:
                active_policy_response = InsurancePolicyResponse(
                    id=policy.id,
                    patient_id=policy.patient_id,
                    provider_id=policy.provider_id,
                    policy_number=policy.policy_number,
                    coverage_details=policy.coverage_details,
                    valid_from=policy.valid_from,
                    valid_until=policy.valid_until,
                    status=policy.status,
                    created_at=policy.created_at,
                    updated_at=policy.updated_at
                )

        logger.info(
            f"Insurance status retrieved for patient {patient.national_id_number}: "
            f"has_policy={policy is not None}, has_active_insurance={has_active_insurance}"
        )

        return InsuranceStatusResponse(
            patient_id=patient_id,
            has_active_insurance=has_active_insurance,
            active_policy=active_policy_response,
            has_policy=policy is not None
        )
