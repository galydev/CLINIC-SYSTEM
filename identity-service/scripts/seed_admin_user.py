"""
Seed script to create the initial RRHH admin user

This script should be run once to create the first RRHH user
who can then create other users through the API.

Usage:
    python scripts/seed_admin_user.py
"""
import asyncio
import sys
from pathlib import Path
from datetime import date

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import bcrypt
from config.database import AsyncSessionLocal
from domain.entities.user import User
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl


async def create_admin_user():
    """Create the initial RRHH admin user"""

    # Admin user data
    national_id_number = "1234567890"
    full_name = "Admin RRHH"
    email = "admin@clinic.com"
    phone = "3001234567"
    birth_date = date(1990, 1, 1)
    address = "Clinic Main Office"
    username = "adminrrhh"  # Alphanumeric only (no underscores or special chars)
    password = "Admin123!"  # Change this in production!

    print("=" * 60)
    print("CREATING INITIAL RRHH ADMIN USER")
    print("=" * 60)
    print(f"\nUser Details:")
    print(f"  National ID: {national_id_number}")
    print(f"  Full Name: {full_name}")
    print(f"  Email: {email}")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"  Role: RRHH")
    print()

    try:
        async with AsyncSessionLocal() as session:
            user_repo = UserRepositoryImpl(session)

            # Check if user already exists
            existing_user = await user_repo.get_by_national_id_number(national_id_number)
            if existing_user:
                print(f"[ERROR] User with national ID {national_id_number} already exists!")
                print(f"  Email: {existing_user.email}")
                print(f"  Username: {existing_user.username}")
                return

            existing_email = await user_repo.get_by_email(email)
            if existing_email:
                print(f"[ERROR] User with email {email} already exists!")
                return

            existing_username = await user_repo.get_by_username(username)
            if existing_username:
                print(f"[ERROR] User with username {username} already exists!")
                return

            # Hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

            # Create user entity
            user = User.create(
                national_id_number=national_id_number,
                full_name=full_name,
                email=email,
                phone=phone,
                birth_date=birth_date,
                address=address,
                username=username,
                hashed_password=hashed_password,
                role_ids=[],
                is_superuser=True
            )

            # Save to database
            created_user = await user_repo.save(user)

            print("[OK] Admin user created successfully!")
            print()
            print("=" * 60)
            print("NEXT STEPS:")
            print("=" * 60)
            print("1. Login with the admin credentials:")
            print(f"   POST http://localhost:8001/api/v1/auth/login")
            print(f"   {{")
            print(f'     "identifier": "{username}" or "{email}",')
            print(f'     "password": "{password}"')
            print(f"   }}")
            print()
            print("2. Use the access token to create new users:")
            print(f"   POST http://localhost:8001/api/v1/auth/register")
            print(f"   Authorization: Bearer <access_token>")
            print()
            print("[WARNING]  IMPORTANT: Change the admin password immediately!")
            print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] Error creating admin user: {e}")
        raise


if __name__ == "__main__":
    print("\n[WARNING]  WARNING: This will create an initial RRHH admin user.")
    print("    Make sure the database is initialized first.")
    response = input("\nDo you want to continue? (yes/no): ")

    if response.lower() in ["yes", "y"]:
        asyncio.run(create_admin_user())
    else:
        print("\nOperation cancelled.")
