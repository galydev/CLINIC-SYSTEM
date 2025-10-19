"""Unit tests for User entity"""
from datetime import datetime
from uuid import UUID

import pytest

from domain.entities.user import User


class TestUserEntity:
    """Test cases for User entity"""

    def test_create_user(self):
        """Test creating a new user"""
        user = User.create(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123",
            full_name="Test User",
            is_superuser=False
        )

        assert isinstance(user.id, UUID)
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.hashed_password == "hashed_password_123"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.is_superuser is False
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert user.last_login is None

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.create(
            email="admin@example.com",
            username="adminuser",
            hashed_password="hashed_password_123",
            full_name="Admin User",
            is_superuser=True
        )

        assert user.is_superuser is True

    def test_update_last_login(self):
        """Test updating last login timestamp"""
        user = User.create(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123",
            full_name="Test User"
        )

        initial_updated_at = user.updated_at
        assert user.last_login is None

        user.update_last_login()

        assert isinstance(user.last_login, datetime)
        assert user.updated_at > initial_updated_at

    def test_deactivate_user(self):
        """Test deactivating a user"""
        user = User.create(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123",
            full_name="Test User"
        )

        assert user.is_active is True
        initial_updated_at = user.updated_at

        user.deactivate()

        assert user.is_active is False
        assert user.updated_at > initial_updated_at

    def test_activate_user(self):
        """Test activating a user"""
        user = User.create(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123",
            full_name="Test User"
        )

        user.deactivate()
        assert user.is_active is False

        user.activate()

        assert user.is_active is True
