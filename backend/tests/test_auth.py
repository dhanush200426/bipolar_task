"""
Authentication tests.
"""
import pytest
from app.core.security import create_access_token


def test_login_success(client, admin_user):
    """Test successful login."""
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "admin@test.com"
    assert data["user"]["role"] == "ADMIN"


def test_login_wrong_password(client, admin_user):
    """Test login with wrong password."""
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_CREDENTIALS"
    assert "message" in data["error"]


def test_login_user_not_found(client, db_session):
    """Test login with non-existent user."""
    response = client.post("/auth/login", json={
        "email": "nonexistent@test.com",
        "password": "password"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "INVALID_CREDENTIALS"


def test_get_me_no_token(client):
    """Test /auth/me without token."""
    response = client.get("/auth/me")
    
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHENTICATED"


def test_get_me_bad_token(client):
    """Test /auth/me with invalid token."""
    response = client.get("/auth/me", headers={
        "Authorization": "Bearer invalid_token"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHENTICATED"


def test_get_me_valid_token(client, admin_user):
    """Test /auth/me with valid token."""
    token = create_access_token(admin_user.id, admin_user.role)
    
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin_user.id
    assert data["email"] == admin_user.email
    assert data["role"] == admin_user.role


def test_member_blocked_from_admin_routes(client, member_user, sample_snack):
    """Test that member cannot access admin routes."""
    token = create_access_token(member_user.id, member_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test POST /snacks (admin only)
    response = client.post("/snacks", json={
        "name": "Test",
        "category": "sweet",
        "quantity": 10
    }, headers=headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"
    
    # Test PATCH /snacks/{id} (admin only)
    response = client.patch(f"/snacks/{sample_snack.id}", json={
        "name": "Updated"
    }, headers=headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"
    
    # Test DELETE /snacks/{id} (admin only)
    response = client.delete(f"/snacks/{sample_snack.id}", headers=headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"
    
    # Test POST /snacks/{id}/restock (admin only)
    response = client.post(f"/snacks/{sample_snack.id}/restock", json={
        "amount": 10
    }, headers=headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"
