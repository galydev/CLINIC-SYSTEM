"""Initialize database using SQLAlchemy ORM models"""
import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config.settings import settings
from infrastructure.database.models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def drop_all_tables():
    """Drop all tables from database"""
    logger.warning("⚠️  Dropping all tables...")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
    logger.info("✅ All tables dropped")


async def create_all_tables():
    """Create all tables from SQLAlchemy models"""
    logger.info("Creating all tables from ORM models...")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        future=True
    )

    async with engine.begin() as conn:
        # This creates all tables defined in the models
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    logger.info("✅ All tables created from ORM models")


async def reset_database(drop_first: bool = True):
    """
    Reset database: drop all tables and create them fresh

    Args:
        drop_first: If True, drop existing tables first (default: True)
    """
    logger.info("=" * 70)
    logger.info("DATABASE RESET - Using SQLAlchemy ORM")
    logger.info("=" * 70)
    logger.info("")

    if drop_first:
        logger.warning("⚠️  WARNING: This will DELETE ALL DATA!")
        logger.info("Waiting 3 seconds... Press Ctrl+C to cancel")
        await asyncio.sleep(3)
        logger.info("")

        await drop_all_tables()
        logger.info("")

    await create_all_tables()

    logger.info("")
    logger.info("=" * 70)
    logger.info("✅ Database reset completed!")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Tables created from models:")
    logger.info("  - genders")
    logger.info("  - blood_types")
    logger.info("  - marital_statuses")
    logger.info("  - relationship_types")
    logger.info("  - insurance_statuses")
    logger.info("  - insurance_providers")
    logger.info("  - patients")
    logger.info("  - emergency_contacts")
    logger.info("  - insurance_policies")
    logger.info("")
    logger.info("Next step: Run seed script to populate catalogs")
    logger.info("  python seed_data.py")
    logger.info("")


async def main():
    """Main entry point"""
    try:
        await reset_database(drop_first=True)
    except Exception as e:
        logger.error(f"❌ Error resetting database: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
