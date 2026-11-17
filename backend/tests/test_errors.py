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


def test_malformed_json_body(client, admin_user):
    """Test malformed JSON body returns clean 422 with VALIDATION_ERROR."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = client.post("/snacks", content=b"{not valid json...", headers=headers)
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "error" in data


def test_expired_token(client):
    """Test expired token returns 401 UNAUTHENTICATED."""
    from datetime import datetime, timedelta
    from jose import jwt
    from app.core.config import settings
    expired_token = jwt.encode(
        {"sub": "user_id", "role": "MEMBER", "exp": datetime.utcnow() - timedelta(minutes=5)},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/snacks", headers=headers)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHENTICATED"


def test_negative_amount_validation(client, member_user, sample_snack):
    """Test negative quantity/amount returns 422 VALIDATION_ERROR."""
    token = create_access_token(member_user.id, member_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/snacks/{sample_snack.id}/consume", json={"amount": -5}, headers=headers)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_sql_injection_search_query(client, member_user):
    """Test SQL injection in search parameter executes safely with 0 matches or normal matches."""
    token = create_access_token(member_user.id, member_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/snacks?q=' OR 1=1 --", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    # SQL injection should NOT return all items; it literally searches for the string
    assert data["total"] == 0 or all("' OR 1=1 --" in item["name"] for item in data["items"])


def test_deleted_snack_while_viewing(client, member_user):
    """Test querying a deleted or nonexistent snack returns 404 SNACK_NOT_FOUND."""
    token = create_access_token(member_user.id, member_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/snacks/00000000-0000-0000-0000-000000000000", headers=headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SNACK_NOT_FOUND"

