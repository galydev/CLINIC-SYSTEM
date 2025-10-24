"""Unit tests for InsurancePolicy entity"""
import pytest
from datetime import date, datetime, timedelta
from uuid import uuid4

from domain.entities.insurance_policy import InsurancePolicy


def test_create_insurance_policy_with_valid_data():
    """Test creating an insurance policy with valid data"""
    patient_id = uuid4()
    provider_id = uuid4()
    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-2024-001",
        coverage_details="Full coverage including dental and vision",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )

    assert policy.patient_id == patient_id
    assert policy.provider_id == provider_id
    assert policy.policy_number == "POL-2024-001"
    assert policy.coverage_details == "Full coverage including dental and vision"
    assert policy.valid_from == date(2024, 1, 1)
    assert policy.valid_until == date(2025, 12, 31)
    assert policy.status == "ACTIVE"
    assert policy.id is not None
    assert isinstance(policy.created_at, datetime)
    assert isinstance(policy.updated_at, datetime)


def test_create_insurance_policy_with_empty_policy_number():
    """Test creating policy with empty policy number fails"""
    patient_id = uuid4()
    provider_id = uuid4()

    with pytest.raises(ValueError, match="Policy number cannot be empty"):
        InsurancePolicy.create(
            patient_id=patient_id,
            provider_id=provider_id,
            policy_number="",
            coverage_details="Coverage",
            valid_from=date(2024, 1, 1),
            valid_until=date(2025, 12, 31)
        )


def test_create_insurance_policy_with_long_policy_number():
    """Test creating policy with policy number too long fails"""
    patient_id = uuid4()
    provider_id = uuid4()

    with pytest.raises(ValueError, match="Policy number must not exceed 50 characters"):
        InsurancePolicy.create(
            patient_id=patient_id,
            provider_id=provider_id,
            policy_number="A" * 51,
            coverage_details="Coverage",
            valid_from=date(2024, 1, 1),
            valid_until=date(2025, 12, 31)
        )


def test_create_insurance_policy_with_empty_coverage():
    """Test creating policy with empty coverage details fails"""
    patient_id = uuid4()
    provider_id = uuid4()

    with pytest.raises(ValueError, match="Coverage details cannot be empty"):
        InsurancePolicy.create(
            patient_id=patient_id,
            provider_id=provider_id,
            policy_number="POL-001",
            coverage_details="",
            valid_from=date(2024, 1, 1),
            valid_until=date(2025, 12, 31)
        )


def test_create_insurance_policy_with_long_coverage():
    """Test creating policy with coverage details too long fails"""
    patient_id = uuid4()
    provider_id = uuid4()

    with pytest.raises(ValueError, match="Coverage details must not exceed 500 characters"):
        InsurancePolicy.create(
            patient_id=patient_id,
            provider_id=provider_id,
            policy_number="POL-001",
            coverage_details="A" * 501,
            valid_from=date(2024, 1, 1),
            valid_until=date(2025, 12, 31)
        )


def test_create_insurance_policy_with_invalid_dates():
    """Test creating policy with valid_from after valid_until fails"""
    patient_id = uuid4()
    provider_id = uuid4()

    with pytest.raises(ValueError, match="Valid from date must be before valid until date"):
        InsurancePolicy.create(
            patient_id=patient_id,
            provider_id=provider_id,
            policy_number="POL-001",
            coverage_details="Coverage",
            valid_from=date(2025, 12, 31),
            valid_until=date(2024, 1, 1)
        )


def test_update_status_to_inactive_before_valid_from():
    """Test update_status sets INACTIVE when before valid_from date"""
    patient_id = uuid4()
    provider_id = uuid4()

    # Create policy that starts in the future
    future_date = date.today() + timedelta(days=30)
    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=future_date,
        valid_until=future_date + timedelta(days=365)
    )

    policy.update_status()

    assert policy.status == "INACTIVE"


def test_update_status_to_expired_after_valid_until():
    """Test update_status sets EXPIRED when after valid_until date"""
    patient_id = uuid4()
    provider_id = uuid4()

    # Create policy that expired in the past
    past_date = date.today() - timedelta(days=365)
    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=past_date - timedelta(days=365),
        valid_until=past_date
    )

    policy.update_status()

    assert policy.status == "EXPIRED"


def test_update_status_to_active_within_valid_range():
    """Test update_status sets ACTIVE when within valid date range"""
    patient_id = uuid4()
    provider_id = uuid4()

    # Create policy valid today
    yesterday = date.today() - timedelta(days=1)
    tomorrow = date.today() + timedelta(days=365)

    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=yesterday,
        valid_until=tomorrow
    )

    policy.update_status()

    assert policy.status == "ACTIVE"


def test_update_status_does_not_change_suspended():
    """Test update_status doesn't change status if SUSPENDED"""
    patient_id = uuid4()
    provider_id = uuid4()

    yesterday = date.today() - timedelta(days=1)
    tomorrow = date.today() + timedelta(days=365)

    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=yesterday,
        valid_until=tomorrow
    )

    policy.suspend()
    policy.update_status()

    assert policy.status == "SUSPENDED"


def test_suspend_policy():
    """Test suspending a policy"""
    import time
    patient_id = uuid4()
    provider_id = uuid4()

    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=date.today(),
        valid_until=date.today() + timedelta(days=365)
    )

    original_updated_at = policy.updated_at
    time.sleep(0.01)

    policy.suspend()

    assert policy.status == "SUSPENDED"
    assert policy.updated_at >= original_updated_at


def test_activate_policy_within_valid_dates():
    """Test activating a policy within valid date range"""
    import time
    patient_id = uuid4()
    provider_id = uuid4()

    yesterday = date.today() - timedelta(days=1)
    tomorrow = date.today() + timedelta(days=365)

    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=yesterday,
        valid_until=tomorrow
    )

    policy.suspend()
    assert policy.status == "SUSPENDED"

    time.sleep(0.01)
    original_updated_at = policy.updated_at

    policy.activate()

    assert policy.status == "ACTIVE"
    assert policy.updated_at >= original_updated_at


def test_activate_policy_outside_valid_dates():
    """Test activating a policy outside valid date range fails"""
    patient_id = uuid4()
    provider_id = uuid4()

    # Create policy that expired
    past_date = date.today() - timedelta(days=365)
    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=past_date - timedelta(days=365),
        valid_until=past_date
    )

    policy.suspend()

    with pytest.raises(ValueError, match="Cannot activate policy outside valid date range"):
        policy.activate()


def test_is_active_returns_true_for_active_policy():
    """Test is_active returns True for active policy"""
    patient_id = uuid4()
    provider_id = uuid4()

    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=date.today(),
        valid_until=date.today() + timedelta(days=365)
    )

    assert policy.is_active() is True


def test_is_active_returns_false_for_suspended_policy():
    """Test is_active returns False for suspended policy"""
    patient_id = uuid4()
    provider_id = uuid4()

    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage",
        valid_from=date.today(),
        valid_until=date.today() + timedelta(days=365)
    )

    policy.suspend()

    assert policy.is_active() is False


def test_to_dict():
    """Test converting policy to dictionary"""
    patient_id = uuid4()
    provider_id = uuid4()

    policy = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-2024-001",
        coverage_details="Full coverage",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )

    policy_dict = policy.to_dict()

    assert policy_dict["id"] == str(policy.id)
    assert policy_dict["patient_id"] == str(patient_id)
    assert policy_dict["provider_id"] == str(provider_id)
    assert policy_dict["policy_number"] == "POL-2024-001"
    assert policy_dict["coverage_details"] == "Full coverage"
    assert policy_dict["valid_from"] == "2024-01-01"
    assert policy_dict["valid_until"] == "2025-12-31"
    assert policy_dict["status"] == "ACTIVE"
    assert "created_at" in policy_dict
    assert "updated_at" in policy_dict


def test_unique_policy_ids():
    """Test that each policy gets a unique ID"""
    patient_id = uuid4()
    provider_id = uuid4()

    policy1 = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-001",
        coverage_details="Coverage 1",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )

    policy2 = InsurancePolicy.create(
        patient_id=patient_id,
        provider_id=provider_id,
        policy_number="POL-002",
        coverage_details="Coverage 2",
        valid_from=date(2024, 1, 1),
        valid_until=date(2025, 12, 31)
    )

    assert policy1.id != policy2.id
