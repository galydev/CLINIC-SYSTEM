"""Integration tests for API routes"""
import pytest
from fastapi.testclient import TestClient


class TestAuthenticationRoutes:
    """Test cases for authentication routes"""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "identity-service"

    def test_register_user_success(self, client: TestClient, sample_user_data: dict):
        """Test successful user registration"""
        response = client.post("/api/v1/register", json=sample_user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["username"] == sample_user_data["username"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client: TestClient, sample_user_data: dict):
        """Test registration with duplicate email"""
        # First registration
        client.post("/api/v1/register", json=sample_user_data)

        # Second registration with same email
        duplicate_data = sample_user_data.copy()
        duplicate_data["username"] = "different_username"

        response = client.post("/api/v1/register", json=duplicate_data)

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_duplicate_username(self, client: TestClient, sample_user_data: dict):
        """Test registration with duplicate username"""
        # First registration
        client.post("/api/v1/register", json=sample_user_data)

        # Second registration with same username
        duplicate_data = sample_user_data.copy()
        duplicate_data["email"] = "different@example.com"

        response = client.post("/api/v1/register", json=duplicate_data)

        assert response.status_code == 400
        assert "already taken" in response.json()["detail"].lower()

    def test_register_invalid_password(self, client: TestClient, sample_user_data: dict):
        """Test registration with invalid password"""
        invalid_data = sample_user_data.copy()
        invalid_data["password"] = "weak"

        response = client.post("/api/v1/register", json=invalid_data)

        assert response.status_code == 400

    def test_login_success(self, client: TestClient, sample_user_data: dict):
        """Test successful login"""
        # Register user
        client.post("/api/v1/register", json=sample_user_data)

        # Login
        login_data = {
            "identifier": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/v1/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    def test_login_with_username(self, client: TestClient, sample_user_data: dict):
        """Test login with username"""
        # Register user
        client.post("/api/v1/register", json=sample_user_data)

        # Login with username
        login_data = {
            "identifier": sample_user_data["username"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/v1/login", json=login_data)

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_invalid_credentials(self, client: TestClient, sample_user_data: dict):
        """Test login with invalid credentials"""
        # Register user
        client.post("/api/v1/register", json=sample_user_data)

        # Login with wrong password
        login_data = {
            "identifier": sample_user_data["email"],
            "password": "WrongPassword123!"
        }
        response = client.post("/api/v1/login", json=login_data)

        assert response.status_code == 401
        assert "invalid credentials" in response.json()["detail"].lower()

    def test_validate_token_success(self, client: TestClient, sample_user_data: dict):
        """Test successful token validation"""
        # Register and login
        client.post("/api/v1/register", json=sample_user_data)
        login_response = client.post("/api/v1/login", json={
            "identifier": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]

        # Validate token
        validate_data = {"token": token}
        response = client.post("/api/v1/validate", json=validate_data)

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert "user_id" in data
        assert data["email"] == sample_user_data["email"]

    def test_validate_invalid_token(self, client: TestClient):
        """Test validation of invalid token"""
        validate_data = {"token": "invalid.token.here"}
        response = client.post("/api/v1/validate", json=validate_data)

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False

    def test_get_current_user(self, client: TestClient, sample_user_data: dict):
        """Test getting current user information"""
        # Register and login
        client.post("/api/v1/register", json=sample_user_data)
        login_response = client.post("/api/v1/login", json={
            "identifier": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["username"] == sample_user_data["username"]

    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test getting current user without token"""
        response = client.get("/api/v1/me")

        assert response.status_code == 403  # FastAPI returns 403 for missing auth

    def test_admin_endpoint_with_superuser(self, client: TestClient, sample_superuser_data: dict):
        """Test admin endpoint with superuser"""
        # Register and login as superuser
        client.post("/api/v1/register", json=sample_superuser_data)
        login_response = client.post("/api/v1/login", json={
            "identifier": sample_superuser_data["email"],
            "password": sample_superuser_data["password"]
        })
        token = login_response.json()["access_token"]

        # Access admin endpoint
        response = client.get(
            "/api/v1/admin/test",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200

    def test_admin_endpoint_with_regular_user(self, client: TestClient, sample_user_data: dict):
        """Test admin endpoint with regular user"""
        # Register and login as regular user
        client.post("/api/v1/register", json=sample_user_data)
        login_response = client.post("/api/v1/login", json={
            "identifier": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]

        # Try to access admin endpoint
        response = client.get(
            "/api/v1/admin/test",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403
