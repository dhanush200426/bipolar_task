"""
Consume and restock tests.
"""
import pytest
from app.core.security import create_access_token
from app.models import Snack, SnackCategory, Activity, ActivityAction
from sqlalchemy import func


def test_consume_success(client, db_session, admin_user, sample_snack):
    """Test successful consume."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    initial_quantity = sample_snack.quantity
    
    response = client.post(f"/snacks/{sample_snack.id}/consume", json={
        "amount": 1
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == initial_quantity - 1
    
    # Verify exactly one activity row was created
    activity_count = db_session.query(Activity).filter(
        Activity.snack_id == sample_snack.id,
        Activity.action == ActivityAction.CONSUMED
    ).count()
    assert activity_count == 1


def test_consume_insufficient_stock(client, db_session, admin_user, sample_snack):
    """Test consume with insufficient stock."""
    # Set quantity to 2
    sample_snack.quantity = 2
    db_session.commit()
    
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    initial_quantity = sample_snack.quantity
    
    response = client.post(f"/snacks/{sample_snack.id}/consume", json={
        "amount": 5  # More than available
    }, headers=headers)
    
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "INSUFFICIENT_STOCK"
    
    # Verify no activity row was created
    activity_count = db_session.query(Activity).filter(
        Activity.snack_id == sample_snack.id,
        Activity.action == ActivityAction.CONSUMED
    ).count()
    assert activity_count == 0
    
    # Verify quantity didn't change
    db_session.refresh(sample_snack)
    assert sample_snack.quantity == initial_quantity


def test_consume_gone_snack(client, db_session, admin_user):
    """Test consume on a gone snack (quantity 0)."""
    import uuid
    snack = Snack(
        id=str(uuid.uuid4()),
        name="Gone Snack",
        category=SnackCategory.SWEET,
        quantity=0,
        low_stock_threshold=5
    )
    db_session.add(snack)
    db_session.commit()
    
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(f"/snacks/{snack.id}/consume", json={
        "amount": 1
    }, headers=headers)
    
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "INSUFFICIENT_STOCK"
    assert "gone" in data["error"]["message"].lower()


def test_consume_amount_validation(client, admin_user, sample_snack):
    """Test consume amount validation."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test amount = 0
    response = client.post(f"/snacks/{sample_snack.id}/consume", json={
        "amount": 0
    }, headers=headers)
    assert response.status_code == 422
    
    # Test negative amount
    response = client.post(f"/snacks/{sample_snack.id}/consume", json={
        "amount": -1
    }, headers=headers)
    assert response.status_code == 422
    
    # Test huge amount
    response = client.post(f"/snacks/{sample_snack.id}/consume", json={
        "amount": 101
    }, headers=headers)
    assert response.status_code == 422
    
    # Test non-integer amount
    response = client.post(f"/snacks/{sample_snack.id}/consume", json={
        "amount": 1.5
    }, headers=headers)
    assert response.status_code == 422


def test_restock_success(client, db_session, admin_user, sample_snack):
    """Test successful restock."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    initial_quantity = sample_snack.quantity
    
    response = client.post(f"/snacks/{sample_snack.id}/restock", json={
        "amount": 10
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == initial_quantity + 10
    
    # Verify activity row was created
    activity_count = db_session.query(Activity).filter(
        Activity.snack_id == sample_snack.id,
        Activity.action == ActivityAction.RESTOCKED
    ).count()
    assert activity_count == 1


def test_restock_admin_only(client, member_user, sample_snack):
    """Test that restock is admin-only."""
    token = create_access_token(member_user.id, member_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(f"/snacks/{sample_snack.id}/restock", json={
        "amount": 10
    }, headers=headers)
    
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"


def test_restock_not_found(client, db_session, admin_user):
    """Test restock on non-existent snack."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/snacks/nonexistent-id/restock", json={
        "amount": 10
    }, headers=headers)
    
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "SNACK_NOT_FOUND"
