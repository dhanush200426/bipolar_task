"""
Error response format tests.
Ensures all errors return {"error":{"code","message"}} shape.
"""
import pytest
from app.core.security import create_access_token


def test_404_unknown_route(client, db_session):
    """Test 404 for unknown route."""
    response = client.get("/nonexistent/route")
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]


def test_422_bad_body(client, admin_user):
    """Test 422 for invalid request body."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Missing required fields
    response = client.post("/snacks", json={}, headers=headers)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "details" in data["error"]
    
    # Invalid enum value
    response = client.post("/snacks", json={
        "name": "Test",
        "category": "invalid_category",
        "quantity": 10
    }, headers=headers)
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_422_invalid_query_params(client, admin_user):
    """Test 422 for invalid query parameters."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Invalid page (negative)
    response = client.get("/snacks?page=-1", headers=headers)
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    
    # Invalid page_size (over 50)
    response = client.get("/snacks?page_size=100", headers=headers)
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_401_unauthenticated(client, db_session):
    """Test 401 for missing authentication."""
    response = client.get("/snacks")
    
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHENTICATED"


def test_403_forbidden(client, member_user, sample_snack):
    """Test 403 for insufficient permissions."""
    token = create_access_token(member_user.id, member_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/snacks", json={
        "name": "Test",
        "category": "sweet",
        "quantity": 10
    }, headers=headers)
    
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
