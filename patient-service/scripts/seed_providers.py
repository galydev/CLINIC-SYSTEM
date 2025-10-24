"""
Seed insurance providers - Simple script to load initial data

Usage:
    python seed_providers.py
"""
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from infrastructure.database.seed_insurance_providers import main
import asyncio

if __name__ == "__main__":
    print("=" * 60)
    print("Insurance Providers Seed Script")
    print("=" * 60)
    print()
    asyncio.run(main())
    print()
    print("=" * 60)
