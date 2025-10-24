"""Reset database - Drop and recreate all tables"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config.database import engine
from infrastructure.database.models import Base


async def reset_database():
    """Drop all tables and recreate them"""
    print("Dropping all existing tables...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    print(">> All tables dropped successfully")

    print("\nCreating new tables with catalog structure...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(">> All tables created successfully")
    print("\n>> Database reset complete!")
    print("\nNext steps:")
    print("   1. Run: python scripts/seed_catalogs.py")
    print("   2. Start your application")


if __name__ == "__main__":
    asyncio.run(reset_database())
