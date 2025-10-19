"""
Database management script

This script provides commands to manage the database:
- reset: Drop all tables and recreate them (WARNING: deletes all data!)
- init: Create tables if they don't exist
- status: Check database connection and show tables

Usage:
    python scripts/manage_database.py reset
    python scripts/manage_database.py init
    python scripts/manage_database.py status
"""
import asyncio
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from config.settings import get_settings
from infrastructure.database.models import Base


async def reset_database():
    """Drop all tables and recreate them"""
    settings = get_settings()

    print("=" * 70)
    print("DATABASE RESET - WARNING: THIS WILL DELETE ALL DATA!")
    print("=" * 70)
    print(f"\nDatabase: {settings.DATABASE_URL.split('@')[-1]}")
    print()

    response = input("Are you ABSOLUTELY sure you want to continue? (type 'yes' to confirm): ")

    if response != 'yes':
        print("\n❌ Operation cancelled.")
        return

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True
    )

    try:
        print("\n[*] Dropping all tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("[OK] All tables dropped successfully\n")

        print("[*] Creating all tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("[OK] All tables created successfully\n")

        print("=" * 70)
        print("DATABASE RESET COMPLETED!")
        print("=" * 70)
        print("\nTables created:")
        print("  ✓ users")
        print("  ✓ roles")
        print("  ✓ user_roles")
        print("\nNext steps:")
        print("  1. Run: python scripts/seed_admin_user.py")
        print("  2. This will create the initial RRHH admin user")
        print("=" * 70)

    except Exception as e:
        print(f"\n[ERROR] Error resetting database: {e}")
        raise
    finally:
        await engine.dispose()


async def init_database():
    """Create tables if they don't exist"""
    settings = get_settings()

    print("=" * 70)
    print("DATABASE INITIALIZATION")
    print("=" * 70)
    print(f"\nDatabase: {settings.DATABASE_URL.split('@')[-1]}")
    print("\nThis will create tables if they don't exist (safe operation)")
    print()

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True
    )

    try:
        print("[*] Creating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("\n[OK] Database initialized successfully!")
        print("\nTables ready:")
        print("  * users")
        print("  * roles")
        print("  * user_roles")

    except Exception as e:
        print(f"\n[ERROR] Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()


async def check_database_status():
    """Check database connection and show existing tables"""
    settings = get_settings()

    print("=" * 70)
    print("DATABASE STATUS")
    print("=" * 70)
    print(f"\nDatabase: {settings.DATABASE_URL.split('@')[-1]}")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True
    )

    try:
        # Test connection
        print("\n[*] Testing database connection...")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
        print("[OK] Database connection successful!")

        # Check tables
        print("\n[*] Checking tables...")
        async with engine.connect() as conn:
            # Get all tables
            result = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()

            if tables:
                print(f"\n[OK] Found {len(tables)} table(s):")
                for table in tables:
                    # Count rows
                    try:
                        count_result = await conn.execute(text(f"SELECT COUNT(*) FROM {table[0]}"))
                        count = count_result.scalar()
                        print(f"  * {table[0]:<20} ({count} rows)")
                    except Exception:
                        print(f"  * {table[0]:<20} (unable to count)")
            else:
                print("\n[WARNING] No tables found. Run 'init' to create them.")

        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\n[ERROR] Error checking database status: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Check DATABASE_URL in .env file")
        print("  3. Verify database credentials")
        raise
    finally:
        await engine.dispose()


def print_usage():
    """Print usage instructions"""
    print("""
Database Management Script
==========================

Usage:
    python scripts/manage_database.py <command>

Commands:
    reset   - Drop all tables and recreate them (⚠️  DELETES ALL DATA!)
    init    - Create tables if they don't exist (safe)
    status  - Check database connection and show tables

Examples:
    python scripts/manage_database.py status
    python scripts/manage_database.py init
    python scripts/manage_database.py reset
""")


async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "reset":
        await reset_database()
    elif command == "init":
        await init_database()
    elif command == "status":
        await check_database_status()
    elif command in ["help", "-h", "--help"]:
        print_usage()
    else:
        print(f"\n❌ Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        sys.exit(1)
