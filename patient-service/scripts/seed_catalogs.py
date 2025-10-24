"""Seed catalog tables with initial data"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy.ext.asyncio import AsyncSession
from config.database import AsyncSessionLocal
from infrastructure.database.models import (
    GenderModel,
    BloodTypeModel,
    MaritalStatusModel,
    RelationshipTypeModel,
    InsuranceStatusModel
)
import uuid


async def seed_genders(session: AsyncSession):
    """Seed genders catalog"""
    genders = [
        {
            "id": uuid.uuid4(),
            "code": "MALE",
            "name": "Male",
            "description": "Male gender"
        },
        {
            "id": uuid.uuid4(),
            "code": "FEMALE",
            "name": "Female",
            "description": "Female gender"
        },
        {
            "id": uuid.uuid4(),
            "code": "OTHER",
            "name": "Other",
            "description": "Other gender"
        }
    ]

    for gender_data in genders:
        gender = GenderModel(**gender_data)
        session.add(gender)

    await session.commit()
    print(f">> Seeded {len(genders)} genders")


async def seed_blood_types(session: AsyncSession):
    """Seed blood types catalog"""
    blood_types = [
        {
            "id": uuid.uuid4(),
            "code": "A+",
            "name": "A+",
            "description": "Blood type A positive"
        },
        {
            "id": uuid.uuid4(),
            "code": "A-",
            "name": "A-",
            "description": "Blood type A negative"
        },
        {
            "id": uuid.uuid4(),
            "code": "B+",
            "name": "B+",
            "description": "Blood type B positive"
        },
        {
            "id": uuid.uuid4(),
            "code": "B-",
            "name": "B-",
            "description": "Blood type B negative"
        },
        {
            "id": uuid.uuid4(),
            "code": "AB+",
            "name": "AB+",
            "description": "Blood type AB positive"
        },
        {
            "id": uuid.uuid4(),
            "code": "AB-",
            "name": "AB-",
            "description": "Blood type AB negative"
        },
        {
            "id": uuid.uuid4(),
            "code": "O+",
            "name": "O+",
            "description": "Blood type O positive"
        },
        {
            "id": uuid.uuid4(),
            "code": "O-",
            "name": "O-",
            "description": "Blood type O negative"
        }
    ]

    for blood_type_data in blood_types:
        blood_type = BloodTypeModel(**blood_type_data)
        session.add(blood_type)

    await session.commit()
    print(f">> Seeded {len(blood_types)} blood types")


async def seed_marital_statuses(session: AsyncSession):
    """Seed marital statuses catalog"""
    marital_statuses = [
        {
            "id": uuid.uuid4(),
            "code": "SINGLE",
            "name": "Single",
            "description": "Never married"
        },
        {
            "id": uuid.uuid4(),
            "code": "MARRIED",
            "name": "Married",
            "description": "Currently married"
        },
        {
            "id": uuid.uuid4(),
            "code": "DIVORCED",
            "name": "Divorced",
            "description": "Legally divorced"
        },
        {
            "id": uuid.uuid4(),
            "code": "WIDOWED",
            "name": "Widowed",
            "description": "Spouse deceased"
        },
        {
            "id": uuid.uuid4(),
            "code": "SEPARATED",
            "name": "Separated",
            "description": "Legally separated"
        }
    ]

    for status_data in marital_statuses:
        status = MaritalStatusModel(**status_data)
        session.add(status)

    await session.commit()
    print(f">> Seeded {len(marital_statuses)} marital statuses")


async def seed_relationship_types(session: AsyncSession):
    """Seed relationship types catalog"""
    relationship_types = [
        {
            "id": uuid.uuid4(),
            "code": "SPOUSE",
            "name": "Spouse",
            "description": "Husband or wife"
        },
        {
            "id": uuid.uuid4(),
            "code": "PARENT",
            "name": "Parent",
            "description": "Mother or father"
        },
        {
            "id": uuid.uuid4(),
            "code": "CHILD",
            "name": "Child",
            "description": "Son or daughter"
        },
        {
            "id": uuid.uuid4(),
            "code": "SIBLING",
            "name": "Sibling",
            "description": "Brother or sister"
        },
        {
            "id": uuid.uuid4(),
            "code": "FRIEND",
            "name": "Friend",
            "description": "Friend"
        },
        {
            "id": uuid.uuid4(),
            "code": "OTHER",
            "name": "Other",
            "description": "Other relationship"
        }
    ]

    for type_data in relationship_types:
        rel_type = RelationshipTypeModel(**type_data)
        session.add(rel_type)

    await session.commit()
    print(f">> Seeded {len(relationship_types)} relationship types")


async def seed_insurance_statuses(session: AsyncSession):
    """Seed insurance statuses catalog"""
    insurance_statuses = [
        {
            "id": uuid.uuid4(),
            "code": "ACTIVE",
            "name": "Active",
            "description": "Insurance policy is active"
        },
        {
            "id": uuid.uuid4(),
            "code": "INACTIVE",
            "name": "Inactive",
            "description": "Insurance policy is inactive"
        },
        {
            "id": uuid.uuid4(),
            "code": "SUSPENDED",
            "name": "Suspended",
            "description": "Insurance policy is temporarily suspended"
        },
        {
            "id": uuid.uuid4(),
            "code": "EXPIRED",
            "name": "Expired",
            "description": "Insurance policy has expired"
        }
    ]

    for status_data in insurance_statuses:
        status = InsuranceStatusModel(**status_data)
        session.add(status)

    await session.commit()
    print(f">> Seeded {len(insurance_statuses)} insurance statuses")


async def main():
    """Main seeding function"""
    print("Starting catalog seeding...")

    async with AsyncSessionLocal() as session:
        try:
            await seed_genders(session)
            await seed_blood_types(session)
            await seed_marital_statuses(session)
            await seed_relationship_types(session)
            await seed_insurance_statuses(session)

            print("\n>> All catalogs seeded successfully!")
        except Exception as e:
            print(f"\n>> Error seeding catalogs: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
