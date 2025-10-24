"""FastAPI dependencies - Dependency injection setup"""
from typing import AsyncGenerator

from application.use_cases.add_emergency_contact import \
    AddEmergencyContactUseCase
from application.use_cases.add_insurance_policy import \
    AddInsurancePolicyUseCase
from application.use_cases.get_insurance_status import \
    GetInsuranceStatusUseCase
from application.use_cases.get_patient import GetPatientUseCase
from application.use_cases.register_patient import RegisterPatientUseCase
from application.use_cases.update_patient import UpdatePatientUseCase
from config.database import AsyncSessionLocal
from fastapi import Depends
from infrastructure.database.repositories.catalog_repository_impl import (
    BloodTypeRepositoryImpl, GenderRepositoryImpl,
    InsuranceStatusRepositoryImpl, MaritalStatusRepositoryImpl,
    RelationshipTypeRepositoryImpl)
from infrastructure.database.repositories.emergency_contact_repository_impl import \
    EmergencyContactRepositoryImpl
from infrastructure.database.repositories.insurance_policy_repository_impl import \
    InsurancePolicyRepositoryImpl
from infrastructure.database.repositories.insurance_provider_repository_impl import \
    InsuranceProviderRepositoryImpl
from infrastructure.database.repositories.patient_repository_impl import \
    PatientRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================================
# DATABASE SESSION DEPENDENCY
# ============================================================================

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# ============================================================================
# REPOSITORY DEPENDENCIES
# ============================================================================

async def get_patient_repository(
    session: AsyncSession = Depends(get_db_session)
) -> PatientRepositoryImpl:
    return PatientRepositoryImpl(session)


async def get_emergency_contact_repository(
    session: AsyncSession = Depends(get_db_session)
) -> EmergencyContactRepositoryImpl:
    return EmergencyContactRepositoryImpl(session)


async def get_insurance_policy_repository(
    session: AsyncSession = Depends(get_db_session)
) -> InsurancePolicyRepositoryImpl:
    return InsurancePolicyRepositoryImpl(session)


async def get_insurance_provider_repository(
    session: AsyncSession = Depends(get_db_session)
) -> InsuranceProviderRepositoryImpl:
    return InsuranceProviderRepositoryImpl(session)


# ============================================================================
# CATALOG REPOSITORY DEPENDENCIES
# ============================================================================

async def get_gender_repository(
    session: AsyncSession = Depends(get_db_session)
) -> GenderRepositoryImpl:
    return GenderRepositoryImpl(session)


async def get_blood_type_repository(
    session: AsyncSession = Depends(get_db_session)
) -> BloodTypeRepositoryImpl:
    return BloodTypeRepositoryImpl(session)


async def get_marital_status_repository(
    session: AsyncSession = Depends(get_db_session)
) -> MaritalStatusRepositoryImpl:
    return MaritalStatusRepositoryImpl(session)


async def get_relationship_type_repository(
    session: AsyncSession = Depends(get_db_session)
) -> RelationshipTypeRepositoryImpl:
    return RelationshipTypeRepositoryImpl(session)


async def get_insurance_status_repository(
    session: AsyncSession = Depends(get_db_session)
) -> InsuranceStatusRepositoryImpl:
    return InsuranceStatusRepositoryImpl(session)


# ============================================================================
# PATIENT USE CASE DEPENDENCIES
# ============================================================================

async def get_register_patient_use_case(
    patient_repository: PatientRepositoryImpl = Depends(get_patient_repository),
    gender_repository: GenderRepositoryImpl = Depends(get_gender_repository),
    blood_type_repository: BloodTypeRepositoryImpl = Depends(get_blood_type_repository),
    marital_status_repository: MaritalStatusRepositoryImpl = Depends(get_marital_status_repository)
) -> RegisterPatientUseCase:
    return RegisterPatientUseCase(
        patient_repository,
        gender_repository,
        blood_type_repository,
        marital_status_repository
    )


async def get_update_patient_use_case(
    patient_repository: PatientRepositoryImpl = Depends(get_patient_repository),
    marital_status_repository: MaritalStatusRepositoryImpl = Depends(get_marital_status_repository)
) -> UpdatePatientUseCase:
    return UpdatePatientUseCase(patient_repository, marital_status_repository)


async def get_get_patient_use_case(
    patient_repository: PatientRepositoryImpl = Depends(get_patient_repository)
) -> GetPatientUseCase:
    return GetPatientUseCase(patient_repository)


# ============================================================================
# EMERGENCY CONTACT USE CASE DEPENDENCIES
# ============================================================================

async def get_add_emergency_contact_use_case(
    emergency_contact_repository: EmergencyContactRepositoryImpl = Depends(
        get_emergency_contact_repository
    ),
    patient_repository: PatientRepositoryImpl = Depends(get_patient_repository),
    relationship_type_repository: RelationshipTypeRepositoryImpl = Depends(
        get_relationship_type_repository
    )
) -> AddEmergencyContactUseCase:
    return AddEmergencyContactUseCase(
        emergency_contact_repository,
        patient_repository,
        relationship_type_repository
    )


# ============================================================================
# INSURANCE POLICY USE CASE DEPENDENCIES
# ============================================================================

async def get_add_insurance_policy_use_case(
    insurance_policy_repository: InsurancePolicyRepositoryImpl = Depends(
        get_insurance_policy_repository
    ),
    insurance_provider_repository: InsuranceProviderRepositoryImpl = Depends(
        get_insurance_provider_repository
    ),
    patient_repository: PatientRepositoryImpl = Depends(get_patient_repository),
    insurance_status_repository: InsuranceStatusRepositoryImpl = Depends(
        get_insurance_status_repository
    )
) -> AddInsurancePolicyUseCase:
    return AddInsurancePolicyUseCase(
        insurance_policy_repository,
        insurance_provider_repository,
        patient_repository,
        insurance_status_repository
    )


async def get_get_insurance_status_use_case(
    insurance_policy_repository: InsurancePolicyRepositoryImpl = Depends(
        get_insurance_policy_repository
    ),
    patient_repository: PatientRepositoryImpl = Depends(get_patient_repository),
) -> GetInsuranceStatusUseCase:
    return GetInsuranceStatusUseCase(insurance_policy_repository, patient_repository)
