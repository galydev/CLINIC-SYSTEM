"""Add insurance policy use case - Application layer business logic"""
import logging
from uuid import UUID

from application.dto.insurance_policy_request import AddInsurancePolicyRequest
from application.dto.insurance_policy_response import InsurancePolicyResponse
from domain.entities.insurance_policy import InsurancePolicy
from domain.repositories.catalog_repository import InsuranceStatusRepository
from domain.repositories.insurance_policy_repository import \
    InsurancePolicyRepository
from domain.repositories.insurance_provider_repository import \
    InsuranceProviderRepository
from domain.repositories.patient_repository import PatientRepository

logger = logging.getLogger(__name__)


class PatientNotFoundError(Exception):
    """Exception raised when patient is not found"""
    pass


class InsuranceProviderNotFoundError(Exception):
    """Exception raised when insurance provider is not found"""
    pass


class DuplicatePolicyError(Exception):
    """Exception raised when policy number already exists or patient already has a policy"""
    pass


class ValidationError(Exception):
    """Exception raised when insurance policy data validation fails"""
    pass


class AddInsurancePolicyUseCase:

    def __init__(
        self,
        insurance_policy_repository: InsurancePolicyRepository,
        insurance_provider_repository: InsuranceProviderRepository,
        patient_repository: PatientRepository,
        insurance_status_repository: InsuranceStatusRepository
    ):
        self.insurance_policy_repository = insurance_policy_repository
        self.insurance_provider_repository = insurance_provider_repository
        self.patient_repository = patient_repository
        self.insurance_status_repository = insurance_status_repository

    async def execute(
        self,
        patient_id: UUID,
        request: AddInsurancePolicyRequest
    ) -> InsurancePolicyResponse:

        try:
            # Verify patient exists
            patient = await self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise PatientNotFoundError(f"Patient with ID {patient_id} not found")

            # CRITICAL: Check if patient already has a policy (ONE POLICY PER PATIENT)
            existing_policies = await self.insurance_policy_repository.get_by_patient_id(patient_id)
            if existing_policies:
                raise DuplicatePolicyError(
                    f"Patient {patient_id} already has an insurance policy. "
                    f"Only one policy per patient is allowed."
                )

            # Verify insurance provider exists
            provider = await self.insurance_provider_repository.get_by_id(request.provider_id)
            if not provider:
                raise InsuranceProviderNotFoundError(
                    f"Insurance provider with ID {request.provider_id} not found"
                )

            # Check policy number uniqueness
            existing_policy = await self.insurance_policy_repository.exists_by_policy_number(
                request.policy_number
            )
            if existing_policy:
                raise DuplicatePolicyError(
                    f"Insurance policy with number {request.policy_number} already exists"
                )

            # Validate insurance status (default to ACTIVE for new policies)
            status_id = await self.insurance_status_repository.get_by_code('ACTIVE')
            if not status_id:
                raise ValidationError(f"Invalid insurance status code: ACTIVE")

            # Create insurance policy entity
            # InsurancePolicy.create validates: policy_number,
            # coverage_details, valid_from < valid_until
            insurance_policy = InsurancePolicy.create(
                patient_id=patient_id,
                provider_id=request.provider_id,
                policy_number=request.policy_number,
                coverage_details=request.coverage_details,
                valid_from=request.valid_from,
                valid_until=request.valid_until
            )

            # Persist insurance policy with validated catalog ID
            created_policy = await self.insurance_policy_repository.save(
                insurance_policy,
                status_id=status_id
            )

            logger.info(
                f"Insurance policy added for patient {patient.national_id_number}: "
                f"{created_policy.policy_number} (Provider: {provider.name})"
            )

            return InsurancePolicyResponse(
                id=created_policy.id,
                patient_id=created_policy.patient_id,
                provider_id=created_policy.provider_id,
                policy_number=created_policy.policy_number,
                coverage_details=created_policy.coverage_details,
                valid_from=created_policy.valid_from,
                valid_until=created_policy.valid_until,
                status=created_policy.status,
                created_at=created_policy.created_at,
                updated_at=created_policy.updated_at
            )

        except ValueError as e:
            logger.error(f"Validation error while adding insurance policy: {str(e)}")
            raise ValidationError(str(e))
        except PatientNotFoundError:
            raise
        except InsuranceProviderNotFoundError:
            raise
        except DuplicatePolicyError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while adding insurance policy: {str(e)}")
            raise
