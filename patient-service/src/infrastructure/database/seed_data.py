"""Seed database with initial catalog data using ORM"""
import asyncio
import logging
from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select

from config.settings import settings
from infrastructure.database.models import (
    GenderModel,
    BloodTypeModel,
    MaritalStatusModel,
    RelationshipTypeModel,
    InsuranceStatusModel,
    InsuranceProviderModel
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_catalogs(session: AsyncSession):
    """Seed all catalog tables"""
    logger.info("Seeding catalog tables...")

    # ============================================================================
    # GENDERS
    # ============================================================================
    genders_data = [
        {"code": "MALE", "name": "Masculino", "description": "Género masculino"},
        {"code": "FEMALE", "name": "Femenino", "description": "Género femenino"},
        {"code": "OTHER", "name": "Otro", "description": "Otro género"}
    ]

    for data in genders_data:
        result = await session.execute(
            select(GenderModel).where(GenderModel.code == data["code"])
        )
        if not result.scalar_one_or_none():
            gender = GenderModel(
                id=uuid4(),
                code=data["code"],
                name=data["name"],
                description=data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(gender)
            logger.info(f"  Created gender: {data['name']}")

    # ============================================================================
    # BLOOD TYPES
    # ============================================================================
    blood_types_data = [
        {"code": "A_POSITIVE", "name": "A+", "description": "Tipo de sangre A positivo"},
        {"code": "A_NEGATIVE", "name": "A-", "description": "Tipo de sangre A negativo"},
        {"code": "B_POSITIVE", "name": "B+", "description": "Tipo de sangre B positivo"},
        {"code": "B_NEGATIVE", "name": "B-", "description": "Tipo de sangre B negativo"},
        {"code": "AB_POSITIVE", "name": "AB+", "description": "Tipo de sangre AB positivo"},
        {"code": "AB_NEGATIVE", "name": "AB-", "description": "Tipo de sangre AB negativo"},
        {"code": "O_POSITIVE", "name": "O+", "description": "Tipo de sangre O positivo"},
        {"code": "O_NEGATIVE", "name": "O-", "description": "Tipo de sangre O negativo"}
    ]

    for data in blood_types_data:
        result = await session.execute(
            select(BloodTypeModel).where(BloodTypeModel.code == data["code"])
        )
        if not result.scalar_one_or_none():
            blood_type = BloodTypeModel(
                id=uuid4(),
                code=data["code"],
                name=data["name"],
                description=data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(blood_type)
            logger.info(f"  Created blood type: {data['name']}")

    # ============================================================================
    # MARITAL STATUSES
    # ============================================================================
    marital_statuses_data = [
        {"code": "SINGLE", "name": "Soltero(a)", "description": "Estado civil: soltero"},
        {"code": "MARRIED", "name": "Casado(a)", "description": "Estado civil: casado"},
        {"code": "DIVORCED", "name": "Divorciado(a)", "description": "Estado civil: divorciado"},
        {"code": "WIDOWED", "name": "Viudo(a)", "description": "Estado civil: viudo"},
        {"code": "SEPARATED", "name": "Separado(a)", "description": "Estado civil: separado"},
        {"code": "COHABITING", "name": "Unión libre", "description": "Estado civil: unión libre"}
    ]

    for data in marital_statuses_data:
        result = await session.execute(
            select(MaritalStatusModel).where(MaritalStatusModel.code == data["code"])
        )
        if not result.scalar_one_or_none():
            status = MaritalStatusModel(
                id=uuid4(),
                code=data["code"],
                name=data["name"],
                description=data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(status)
            logger.info(f"  Created marital status: {data['name']}")

    # ============================================================================
    # RELATIONSHIP TYPES
    # ============================================================================
    relationship_types_data = [
        {"code": "SPOUSE", "name": "Cónyuge", "description": "Esposo(a) o pareja"},
        {"code": "PARENT", "name": "Padre/Madre", "description": "Progenitor"},
        {"code": "CHILD", "name": "Hijo(a)", "description": "Descendiente directo"},
        {"code": "SIBLING", "name": "Hermano(a)", "description": "Hermano o hermana"},
        {"code": "FRIEND", "name": "Amigo(a)", "description": "Amistad cercana"},
        {"code": "GRANDPARENT", "name": "Abuelo(a)", "description": "Abuelo o abuela"},
        {"code": "GRANDCHILD", "name": "Nieto(a)", "description": "Nieto o nieta"},
        {"code": "UNCLE_AUNT", "name": "Tío(a)", "description": "Tío o tía"},
        {"code": "COUSIN", "name": "Primo(a)", "description": "Primo o prima"},
        {"code": "OTHER", "name": "Otro", "description": "Otra relación"}
    ]

    for data in relationship_types_data:
        result = await session.execute(
            select(RelationshipTypeModel).where(RelationshipTypeModel.code == data["code"])
        )
        if not result.scalar_one_or_none():
            rel_type = RelationshipTypeModel(
                id=uuid4(),
                code=data["code"],
                name=data["name"],
                description=data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(rel_type)
            logger.info(f"  Created relationship type: {data['name']}")

    # ============================================================================
    # INSURANCE STATUSES
    # ============================================================================
    insurance_statuses_data = [
        {"code": "ACTIVE", "name": "Activo", "description": "Póliza activa y vigente"},
        {"code": "INACTIVE", "name": "Inactivo", "description": "Póliza inactiva (aún no inicia vigencia)"},
        {"code": "SUSPENDED", "name": "Suspendido", "description": "Póliza suspendida temporalmente"},
        {"code": "EXPIRED", "name": "Expirado", "description": "Póliza vencida"}
    ]

    for data in insurance_statuses_data:
        result = await session.execute(
            select(InsuranceStatusModel).where(InsuranceStatusModel.code == data["code"])
        )
        if not result.scalar_one_or_none():
            status = InsuranceStatusModel(
                id=uuid4(),
                code=data["code"],
                name=data["name"],
                description=data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(status)
            logger.info(f"  Created insurance status: {data['name']}")

    await session.commit()
    logger.info("✅ Catalogs seeded successfully")


async def seed_insurance_providers(session: AsyncSession):
    """Seed insurance providers"""
    logger.info("Seeding insurance providers...")

    providers_data = [
        {"name": "SaludTotal", "code": "SALUDTOTAL", "phone": "50422345678",
         "email": "contacto@saludtotal.hn", "website": "https://www.saludtotal.hn",
         "address": "Tegucigalpa, Honduras"},
        {"name": "MediPlus", "code": "MEDIPLUS", "phone": "50422456789",
         "email": "info@mediplus.hn", "website": "https://www.mediplus.hn",
         "address": "San Pedro Sula, Honduras"},
        {"name": "VidaSana Seguros", "code": "VIDASANA", "phone": "50422567890",
         "email": "contacto@vidasana.hn", "website": "https://www.vidasana.hn",
         "address": "Tegucigalpa, Honduras"},
        {"name": "AsistMed", "code": "ASISTMED", "phone": "50422678901",
         "email": "soporte@asistmed.hn", "website": "https://www.asistmed.hn",
         "address": "Tegucigalpa, Honduras"},
        {"name": "Seguros Médicos del Pacífico", "code": "PACIFICO", "phone": "50422789012",
         "email": "info@pacifico.hn", "website": "https://www.pacifico.hn",
         "address": "Tegucigalpa, Honduras"},
        {"name": "Atlas Seguros", "code": "ATLAS", "phone": "50422890123",
         "email": "contacto@atlas.hn", "website": "https://www.atlas.hn",
         "address": "San Pedro Sula, Honduras"},
        {"name": "Seguros Crefisa", "code": "CREFISA", "phone": "50422901234",
         "email": "info@crefisa.hn", "website": "https://www.crefisa.hn",
         "address": "Tegucigalpa, Honduras"},
        {"name": "Seguros FICOHSA", "code": "FICOHSA", "phone": "50422012345",
         "email": "seguros@ficohsa.hn", "website": "https://www.ficohsa.hn",
         "address": "Tegucigalpa, Honduras"},
        {"name": "Pan-American Life Insurance", "code": "PALIC", "phone": "50422123456",
         "email": "info@palic.hn", "website": "https://www.palic.com",
         "address": "Tegucigalpa, Honduras"},
        {"name": "Seguros del País", "code": "DELPAIS", "phone": "50422234567",
         "email": "contacto@delpais.hn", "website": "https://www.delpais.hn",
         "address": "San Pedro Sula, Honduras"},
        {"name": "Seguros Privados", "code": "PRIVADOS", "phone": "50422345670",
         "email": "info@privados.hn", "website": None,
         "address": "Tegucigalpa, Honduras"},
        {"name": "Sin Seguro", "code": "NINGUNO", "phone": None,
         "email": None, "website": None, "address": None}
    ]

    for data in providers_data:
        result = await session.execute(
            select(InsuranceProviderModel).where(InsuranceProviderModel.code == data["code"])
        )
        if not result.scalar_one_or_none():
            provider = InsuranceProviderModel(
                id=uuid4(),
                name=data["name"],
                code=data["code"],
                phone=data.get("phone"),
                email=data.get("email"),
                website=data.get("website"),
                address=data.get("address"),
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(provider)
            logger.info(f"  Created provider: {data['name']} ({data['code']})")

    await session.commit()
    logger.info("✅ Insurance providers seeded successfully")


async def seed_all():
    """Seed all data"""
    logger.info("=" * 70)
    logger.info("DATABASE SEED - Using SQLAlchemy ORM")
    logger.info("=" * 70)
    logger.info("")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        future=True
    )

    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        try:
            await seed_catalogs(session)
            logger.info("")
            await seed_insurance_providers(session)

            logger.info("")
            logger.info("=" * 70)
            logger.info("✅ All data seeded successfully!")
            logger.info("=" * 70)
            logger.info("")
            logger.info("Summary:")
            logger.info("  - 3 genders")
            logger.info("  - 8 blood types")
            logger.info("  - 6 marital statuses")
            logger.info("  - 10 relationship types")
            logger.info("  - 4 insurance statuses")
            logger.info("  - 12 insurance providers")
            logger.info("")

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Error seeding data: {str(e)}")
            raise
        finally:
            await engine.dispose()


async def main():
    """Main entry point"""
    try:
        await seed_all()
    except Exception as e:
        logger.error(f"Failed to seed data: {str(e)}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
