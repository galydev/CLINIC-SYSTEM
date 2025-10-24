"""Seed script for insurance providers - Initial data load"""
import asyncio
import logging
from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select

from config.settings import settings
from infrastructure.database.models.insurance_provider_model import InsuranceProviderModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Insurance providers seed data for Honduras/Central America
INSURANCE_PROVIDERS = [
    {
        "name": "SaludTotal",
        "code": "SALUDTOTAL",
        "phone": "50422345678",
        "email": "contacto@saludtotal.hn",
        "website": "https://www.saludtotal.hn",
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "MediPlus",
        "code": "MEDIPLUS",
        "phone": "50422456789",
        "email": "info@mediplus.hn",
        "website": "https://www.mediplus.hn",
        "address": "San Pedro Sula, Honduras",
        "is_active": True
    },
    {
        "name": "VidaSana Seguros",
        "code": "VIDASANA",
        "phone": "50422567890",
        "email": "contacto@vidasana.hn",
        "website": "https://www.vidasana.hn",
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "AsistMed",
        "code": "ASISTMED",
        "phone": "50422678901",
        "email": "soporte@asistmed.hn",
        "website": "https://www.asistmed.hn",
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "Seguros Médicos del Pacífico",
        "code": "PACIFICO",
        "phone": "50422789012",
        "email": "info@pacifico.hn",
        "website": "https://www.pacifico.hn",
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "Atlas Seguros",
        "code": "ATLAS",
        "phone": "50422890123",
        "email": "contacto@atlas.hn",
        "website": "https://www.atlas.hn",
        "address": "San Pedro Sula, Honduras",
        "is_active": True
    },
    {
        "name": "Seguros Crefisa",
        "code": "CREFISA",
        "phone": "50422901234",
        "email": "info@crefisa.hn",
        "website": "https://www.crefisa.hn",
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "Seguros FICOHSA",
        "code": "FICOHSA",
        "phone": "50422012345",
        "email": "seguros@ficohsa.hn",
        "website": "https://www.ficohsa.hn",
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "Pan-American Life Insurance",
        "code": "PALIC",
        "phone": "50422123456",
        "email": "info@palic.hn",
        "website": "https://www.palic.com",
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "Seguros del País",
        "code": "DELPAIS",
        "phone": "50422234567",
        "email": "contacto@delpais.hn",
        "website": "https://www.delpais.hn",
        "address": "San Pedro Sula, Honduras",
        "is_active": True
    },
    {
        "name": "Seguros Privados",
        "code": "PRIVADOS",
        "phone": "50422345670",
        "email": "info@privados.hn",
        "website": None,
        "address": "Tegucigalpa, Honduras",
        "is_active": True
    },
    {
        "name": "Sin Seguro",
        "code": "NINGUNO",
        "phone": None,
        "email": None,
        "website": None,
        "address": None,
        "is_active": True
    }
]


async def seed_insurance_providers():
    """Seed insurance providers into the database"""
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        future=True
    )

    # Create async session maker
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        try:
            logger.info("Starting insurance providers seed...")

            for provider_data in INSURANCE_PROVIDERS:
                # Check if provider already exists
                result = await session.execute(
                    select(InsuranceProviderModel)
                    .where(InsuranceProviderModel.code == provider_data["code"])
                )
                existing_provider = result.scalar_one_or_none()

                if existing_provider:
                    logger.info(f"Provider '{provider_data['name']}' ({provider_data['code']}) already exists, skipping...")
                    continue

                # Create new provider
                provider = InsuranceProviderModel(
                    id=uuid4(),
                    name=provider_data["name"],
                    code=provider_data["code"],
                    phone=provider_data.get("phone"),
                    email=provider_data.get("email"),
                    website=provider_data.get("website"),
                    address=provider_data.get("address"),
                    is_active=provider_data["is_active"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )

                session.add(provider)
                logger.info(f"Created provider: {provider_data['name']} ({provider_data['code']})")

            await session.commit()
            logger.info("✅ Insurance providers seed completed successfully!")

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Error seeding insurance providers: {str(e)}")
            raise
        finally:
            await engine.dispose()


async def main():
    """Main entry point"""
    try:
        await seed_insurance_providers()
    except Exception as e:
        logger.error(f"Failed to seed insurance providers: {str(e)}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
