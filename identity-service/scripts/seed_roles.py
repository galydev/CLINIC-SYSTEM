"""Seed initial roles in the database"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config.database import get_db_session, engine
from domain.entities.role import Role
from infrastructure.database.repositories.role_repository_impl import RoleRepositoryImpl


# Initial roles to seed
INITIAL_ROLES = [
    {
        "code": "RRHH",
        "name": "Recursos Humanos",
        "description": "Personal de recursos humanos con permisos completos para gestión de usuarios"
    },
    {
        "code": "ADMIN",
        "name": "Administrador",
        "description": "Administrador del sistema con permisos elevados"
    },
    {
        "code": "MEDICO",
        "name": "Médico",
        "description": "Personal médico con acceso a funcionalidades clínicas"
    },
    {
        "code": "ENFERMERA",
        "name": "Enfermera/Enfermero",
        "description": "Personal de enfermería con acceso a funcionalidades de atención"
    },
    {
        "code": "SOPORTE",
        "name": "Soporte Técnico",
        "description": "Personal de soporte técnico del sistema"
    },
    {
        "code": "USER",
        "name": "Usuario",
        "description": "Usuario estándar con permisos básicos"
    }
]


async def seed_roles():
    """Seed initial roles into the database"""
    print("=" * 60)
    print("Seeding Initial Roles")
    print("=" * 60)

    async for session in get_db_session():
        try:
            role_repository = RoleRepositoryImpl(session)

            created_count = 0
            existing_count = 0
            error_count = 0

            for role_data in INITIAL_ROLES:
                try:
                    # Check if role already exists
                    existing_role = await role_repository.get_by_code(role_data["code"])

                    if existing_role:
                        print(f"[SKIP] Role '{role_data['code']}' already exists")
                        existing_count += 1
                        continue

                    # Create new role
                    role = Role.create(
                        name=role_data["name"],
                        code=role_data["code"],
                        description=role_data["description"]
                    )

                    # Save to database
                    await role_repository.create(role)
                    print(f"[OK] Created role '{role_data['code']}' - {role_data['name']}")
                    created_count += 1

                except Exception as e:
                    print(f"[ERROR] Failed to create role '{role_data['code']}': {e}")
                    error_count += 1

            print("\n" + "=" * 60)
            print("Seed Summary:")
            print(f"  - Roles created: {created_count}")
            print(f"  - Roles already existing: {existing_count}")
            print(f"  - Errors: {error_count}")
            print("=" * 60)

            if error_count > 0:
                return 1

            return 0

        except Exception as e:
            print(f"\n[ERROR] Unexpected error during seeding: {e}")
            import traceback
            traceback.print_exc()
            return 1


async def verify_roles():
    """Verify all roles were created successfully"""
    print("\n" + "=" * 60)
    print("Verifying Roles")
    print("=" * 60)

    async for session in get_db_session():
        try:
            role_repository = RoleRepositoryImpl(session)

            print("\nRoles in database:")
            print("-" * 60)

            roles = await role_repository.get_all(skip=0, limit=100, only_active=True)

            if not roles:
                print("  [WARNING] No roles found in database")
                return 1

            for role in roles:
                status = "[ACTIVE]" if role.is_active else "[INACTIVE]"
                print(f"  {status} {role.code:<15} - {role.name}")
                if role.description:
                    print(f"       Description: {role.description}")

            print("-" * 60)
            print(f"Total roles: {len(roles)}")
            print("=" * 60)

            return 0

        except Exception as e:
            print(f"\n[ERROR] Failed to verify roles: {e}")
            import traceback
            traceback.print_exc()
            return 1


async def main():
    """Main function"""
    try:
        # Seed roles
        exit_code = await seed_roles()

        if exit_code != 0:
            print("\n[FAILED] Seeding failed with errors")
            return exit_code

        # Verify roles
        exit_code = await verify_roles()

        if exit_code != 0:
            print("\n[FAILED] Verification failed")
            return exit_code

        print("\n[SUCCESS] All roles seeded and verified successfully!")
        return 0

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Dispose engine
        await engine.dispose()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
