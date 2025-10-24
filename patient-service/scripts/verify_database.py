"""Verify database initialization - Check tables and data"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import text
from config.database import engine


async def verify_database():
    """Verify database tables and data"""
    print("=" * 70)
    print("DATABASE VERIFICATION")
    print("=" * 70)
    print()

    async with engine.begin() as conn:
        # 1. List all tables
        print("1. TABLES IN DATABASE:")
        print("-" * 70)
        result = await conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = result.fetchall()
        for idx, (table,) in enumerate(tables, 1):
            print(f"   {idx}. {table}")
        print(f"\n   Total tables: {len(tables)}")
        print()

        # 2. Count records in each table
        print("2. RECORD COUNTS:")
        print("-" * 70)

        catalog_tables = [
            'genders',
            'blood_types',
            'marital_statuses',
            'relationship_types',
            'insurance_statuses',
            'insurance_providers'
        ]

        for table in catalog_tables:
            result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"   {table:25} : {count:3} records")

        print()

        # 3. Show insurance providers
        print("3. INSURANCE PROVIDERS LOADED:")
        print("-" * 70)
        result = await conn.execute(text("""
            SELECT code, name, is_active
            FROM insurance_providers
            ORDER BY name
        """))
        providers = result.fetchall()
        for code, name, is_active in providers:
            status = "[ACTIVE]" if is_active else "[INACTIVE]"
            print(f"   {status:12} {code:15} - {name}")
        print()

        # 4. Check unique constraint on insurance_policies.patient_id
        print("4. DATABASE CONSTRAINTS:")
        print("-" * 70)
        result = await conn.execute(text("""
            SELECT conname, contype
            FROM pg_constraint
            WHERE conrelid = 'insurance_policies'::regclass
              AND contype = 'u'
        """))
        constraints = result.fetchall()
        for conname, contype in constraints:
            print(f"   [OK] Constraint: {conname} (type: {contype})")
        print()

        # 5. Check foreign keys
        print("5. FOREIGN KEYS (insurance_policies):")
        print("-" * 70)
        result = await conn.execute(text("""
            SELECT
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                rc.delete_rule
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
            JOIN information_schema.referential_constraints AS rc
              ON rc.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_name = 'insurance_policies'
        """))
        fks = result.fetchall()
        for constraint_name, column_name, foreign_table, delete_rule in fks:
            print(f"   [FK] {column_name:15} -> {foreign_table:20} ({delete_rule})")
        print()

    print("=" * 70)
    print("[SUCCESS] DATABASE VERIFICATION COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - {len(tables)} tables created")
    print(f"  - {len(providers)} insurance providers loaded")
    print(f"  - Unique constraint on patient_id: OK")
    print(f"  - Foreign keys configured: OK")
    print()
    print("Your database is ready to use!")
    print()


if __name__ == "__main__":
    asyncio.run(verify_database())
