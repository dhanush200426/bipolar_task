"""
Vote and unvote tests.
"""
import pytest
from app.core.security import create_access_token
from app.models import Vote


def test_vote_success(client, db_session, admin_user, sample_snack):
    """Test successful vote."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(f"/snacks/{sample_snack.id}/vote", headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["vote_count"] == 1
    assert data["voted_by_me"] is True
    
    # Verify vote row exists
    vote = db_session.query(Vote).filter(
        Vote.user_id == admin_user.id,
        Vote.snack_id == sample_snack.id
    ).first()
    assert vote is not None


def test_vote_already_voted(client, db_session, admin_user, sample_snack):
    """Test voting twice on same snack."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First vote
    response = client.post(f"/snacks/{sample_snack.id}/vote", headers=headers)
    assert response.status_code == 201
    
    # Second vote
    response = client.post(f"/snacks/{sample_snack.id}/vote", headers=headers)
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "ALREADY_VOTED"


def test_vote_not_found(client, db_session, admin_user):
    """Test voting on non-existent snack."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/snacks/nonexistent-id/vote", headers=headers)
    
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "SNACK_NOT_FOUND"


def test_unvote_success(client, db_session, admin_user, sample_snack):
    """Test successful unvote."""
    # First vote
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    client.post(f"/snacks/{sample_snack.id}/vote", headers=headers)
    
    # Then unvote
    response = client.delete(f"/snacks/{sample_snack.id}/vote", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["vote_count"] == 0
    assert data["voted_by_me"] is False
    
    # Verify vote row is deleted
    vote = db_session.query(Vote).filter(
        Vote.user_id == admin_user.id,
        Vote.snack_id == sample_snack.id
    ).first()
    assert vote is None


def test_unvote_not_found(client, db_session, admin_user, sample_snack):
    """Test unvoting when no vote exists."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete(f"/snacks/{sample_snack.id}/vote", headers=headers)
    
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "VOTE_NOT_FOUND"


def test_unvote_twice(client, db_session, admin_user, sample_snack):
    """Test unvoting twice (second should return 404)."""
    # First vote
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    client.post(f"/snacks/{sample_snack.id}/vote", headers=headers)
    
    # First unvote
    response = client.delete(f"/snacks/{sample_snack.id}/vote", headers=headers)
    assert response.status_code == 200
    
    # Second unvote
    response = client.delete(f"/snacks/{sample_snack.id}/vote", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "VOTE_NOT_FOUND"
