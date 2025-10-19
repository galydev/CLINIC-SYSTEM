"""Test script to demonstrate entity validations"""
import sys
import io
from pathlib import Path
from datetime import date
from uuid import uuid4

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from domain.entities.user import User
from domain.entities.role import Role


def test_role_creation():
    """Test role creation"""
    print("\n" + "="*60)
    print("TESTING ROLE ENTITY")
    print("="*60)

    # Valid role
    try:
        role = Role.create(
            name="Doctor",
            code="DOCTOR",
            description="Medical doctor with full privileges"
        )
        print(f"✅ Role created successfully: {role.name} ({role.code})")
        print(f"   ID: {role.id}")
        print(f"   Active: {role.is_active}")
    except Exception as e:
        print(f"❌ Failed to create role: {e}")


def test_user_validations():
    """Test user entity validations"""
    print("\n" + "="*60)
    print("TESTING USER ENTITY VALIDATIONS")
    print("="*60)

    # Test 1: Valid user
    print("\n1. Testing VALID user creation:")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Dr. Juan Pérez García",
            email="juan.perez@clinic.com",
            phone="3001234567",
            birth_date=date(1985, 5, 15),
            address="Calle 123 #45-67",
            username="jperez",
            hashed_password="$2b$12$hashed_password_here",
            role_ids=[uuid4()]
        )
        print(f"✅ User created successfully")
        print(f"   Cedula: {user.cedula}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Roles: {len(user.role_ids)} role(s)")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    # Test 2: Invalid cedula (too long)
    print("\n2. Testing INVALID cedula (11 digits):")
    try:
        user = User.create(
            cedula="12345678901",  # 11 digits - INVALID
            full_name="Test User",
            email="test@clinic.com",
            phone="3001234567",
            birth_date=date(1990, 1, 1),
            address="Address 123",
            username="testuser",
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 3: Invalid cedula (non-numeric)
    print("\n3. Testing INVALID cedula (contains letters):")
    try:
        user = User.create(
            cedula="123ABC7890",  # Contains letters - INVALID
            full_name="Test User",
            email="test@clinic.com",
            phone="3001234567",
            birth_date=date(1990, 1, 1),
            address="Address 123",
            username="testuser",
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 4: Invalid email
    print("\n4. Testing INVALID email format:")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Test User",
            email="invalid-email",  # Invalid format - INVALID
            phone="3001234567",
            birth_date=date(1990, 1, 1),
            address="Address 123",
            username="testuser",
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 5: Invalid phone (too long)
    print("\n5. Testing INVALID phone (11 digits):")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Test User",
            email="test@clinic.com",
            phone="30012345678",  # 11 digits - INVALID
            birth_date=date(1990, 1, 1),
            address="Address 123",
            username="testuser",
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 6: Invalid birth date (future)
    print("\n6. Testing INVALID birth date (in the future):")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Test User",
            email="test@clinic.com",
            phone="3001234567",
            birth_date=date(2030, 1, 1),  # Future date - INVALID
            address="Address 123",
            username="testuser",
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 7: Invalid birth date (too old)
    print("\n7. Testing INVALID birth date (over 150 years):")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Test User",
            email="test@clinic.com",
            phone="3001234567",
            birth_date=date(1850, 1, 1),  # Over 150 years - INVALID
            address="Address 123",
            username="testuser",
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 8: Invalid address (too long)
    print("\n8. Testing INVALID address (over 30 chars):")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Test User",
            email="test@clinic.com",
            phone="3001234567",
            birth_date=date(1990, 1, 1),
            address="This is a very long address that exceeds thirty characters",  # Too long - INVALID
            username="testuser",
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 9: Invalid username (too long)
    print("\n9. Testing INVALID username (over 15 chars):")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Test User",
            email="test@clinic.com",
            phone="3001234567",
            birth_date=date(1990, 1, 1),
            address="Address 123",
            username="verylongusername123",  # 20 chars - INVALID
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")

    # Test 10: Invalid username (contains special chars)
    print("\n10. Testing INVALID username (special characters):")
    try:
        user = User.create(
            cedula="1234567890",
            full_name="Test User",
            email="test@clinic.com",
            phone="3001234567",
            birth_date=date(1990, 1, 1),
            address="Address 123",
            username="user@name",  # Contains @ - INVALID
            hashed_password="$2b$12$hash"
        )
        print(f"❌ Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")


def test_password_validation():
    """Test password validation"""
    print("\n" + "="*60)
    print("TESTING PASSWORD VALIDATION")
    print("="*60)

    test_cases = [
        ("MyPass123!", True, "Valid password"),
        ("short", False, "Too short (< 8 chars)"),
        ("nouppercase123!", False, "No uppercase letter"),
        ("NOLOWERCASE123!", False, "No lowercase letter (implicit)"),
        ("NoNumber!", False, "No number"),
        ("NoSpecial123", False, "No special character"),
        ("MyP@ssw0rd", True, "Valid password with @"),
        ("Str0ng#Pass", True, "Valid password with #"),
    ]

    for password, should_pass, description in test_cases:
        try:
            User.validate_password(password)
            if should_pass:
                print(f"✅ {description}: '{password}'")
            else:
                print(f"❌ {description}: '{password}' - Should have failed!")
        except ValueError as e:
            if not should_pass:
                print(f"✅ {description}: Correctly rejected")
                print(f"   Reason: {e}")
            else:
                print(f"❌ {description}: '{password}' - Should have passed!")
                print(f"   Error: {e}")


def test_user_methods():
    """Test user entity methods"""
    print("\n" + "="*60)
    print("TESTING USER ENTITY METHODS")
    print("="*60)

    # Create user
    user = User.create(
        cedula="1234567890",
        full_name="Dr. María González",
        email="maria.gonzalez@clinic.com",
        phone="3009876543",
        birth_date=date(1988, 8, 20),
        address="Carrera 7 #12-34",
        username="mgonzalez",
        hashed_password="$2b$12$hash",
        role_ids=[]
    )

    # Test add_role
    print("\n1. Testing add_role:")
    role_id_1 = uuid4()
    role_id_2 = uuid4()
    user.add_role(role_id_1)
    user.add_role(role_id_2)
    print(f"✅ Added 2 roles. Total roles: {len(user.role_ids)}")

    # Test has_role
    print("\n2. Testing has_role:")
    if user.has_role(role_id_1):
        print(f"✅ User has role {role_id_1}")
    else:
        print(f"❌ User should have role {role_id_1}")

    # Test remove_role
    print("\n3. Testing remove_role:")
    user.remove_role(role_id_1)
    print(f"✅ Removed role. Total roles: {len(user.role_ids)}")

    # Test to_dict
    print("\n4. Testing to_dict:")
    user_dict = user.to_dict()
    print(f"✅ User dictionary:")
    for key, value in user_dict.items():
        if key != "role_ids":
            print(f"   {key}: {value}")

    # Test update_profile
    print("\n5. Testing update_profile:")
    user.update_profile(
        phone="3111111111",
        address="New Address 456"
    )
    print(f"✅ Profile updated:")
    print(f"   New phone: {user.phone}")
    print(f"   New address: {user.address}")

    # Test deactivate/activate
    print("\n6. Testing deactivate/activate:")
    user.deactivate()
    print(f"✅ User deactivated. Active: {user.is_active}")
    user.activate()
    print(f"✅ User activated. Active: {user.is_active}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("IDENTITY SERVICE - ENTITY VALIDATION TESTS")
    print("="*60)

    test_role_creation()
    test_user_validations()
    test_password_validation()
    test_user_methods()

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")
