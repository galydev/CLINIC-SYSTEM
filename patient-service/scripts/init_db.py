"""
Initialize database using SQLAlchemy ORM

This script:
1. Drops all existing tables (WARNING: deletes all data!)
2. Creates all tables from ORM models
3. Seeds catalog data and insurance providers

Usage:
    python init_db.py
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
from infrastructure.database.init_database import reset_database
from infrastructure.database.seed_data import seed_all


async def main():
    print("=" * 70)
    print("PATIENT SERVICE - DATABASE INITIALIZATION")
    print("=" * 70)
    print()
    print("This will:")
    print("  1. Drop all existing tables (⚠️  ALL DATA WILL BE LOST)")
    print("  2. Create tables from ORM models")
    print("  3. Seed catalogs and insurance providers")
    print()

    # Step 1: Reset database (drop and create tables)
    await reset_database(drop_first=True)

    print()

    # Step 2: Seed data
    await seed_all()

    print("=" * 70)
    print("✅ DATABASE INITIALIZATION COMPLETE!")
    print("=" * 70)
    print()
    print("Your database is ready to use!")
    print("Start your application with: python src/main.py")
    print()


if __name__ == "__main__":
    asyncio.run(main())
