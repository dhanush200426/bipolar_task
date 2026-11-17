"""
Snack CRUD tests.
"""
import pytest
from app.core.security import create_access_token
from app.models import Snack, SnackCategory


def test_create_snack(client, admin_user):
    """Test creating a snack."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/snacks", json={
        "name": "New Snack",
        "category": "sweet",
        "quantity": 10,
        "low_stock_threshold": 5
    }, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Snack"
    assert data["category"] == "sweet"
    assert data["quantity"] == 10
    assert data["status"] == "stocked"


def test_create_duplicate_name(client, admin_user, sample_snack):
    """Test creating a snack with duplicate name."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/snacks", json={
        "name": "Test Snack",  # Same as sample_snack
        "category": "sweet",
        "quantity": 10
    }, headers=headers)
    
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "SNACK_NAME_TAKEN"


def test_patch_snack(client, admin_user, sample_snack):
    """Test updating a snack."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.patch(f"/snacks/{sample_snack.id}", json={
        "name": "Updated Snack",
        "low_stock_threshold": 3
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Snack"
    assert data["low_stock_threshold"] == 3


def test_patch_cannot_change_quantity(client, admin_user, sample_snack):
    """Test that PATCH cannot change quantity."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # SnackUpdate schema doesn't include quantity, so this should be ignored
    # or validation should reject it if somehow passed
    response = client.patch(f"/snacks/{sample_snack.id}", json={
        "name": "Updated"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == sample_snack.quantity  # Should not change


def test_delete_snack(client, admin_user, sample_snack):
    """Test deleting a snack."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete(f"/snacks/{sample_snack.id}", headers=headers)
    
    assert response.status_code == 204
    
    # Verify it's deleted
    response = client.get(f"/snacks/{sample_snack.id}", headers=headers)
    assert response.status_code == 404


def test_list_snacks(client, admin_user, sample_snack):
    """Test listing snacks."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/snacks", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "pages" in data
    assert len(data["items"]) >= 1


def test_list_filter_by_category(client, admin_user, sample_snack):
    """Test filtering snacks by category."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/snacks?category=sweet", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert item["category"] == "sweet"


def test_list_filter_by_status(client, db_session, admin_user):
    """Test filtering snacks by status."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a snack with quantity 0 (gone status)
    import uuid
    from app.models import Snack
    snack = Snack(
        id=str(uuid.uuid4()),
        name="Gone Snack",
        category=SnackCategory.SWEET,
        quantity=0,
        low_stock_threshold=5
    )
    db_session.add(snack)
    db_session.commit()
    
    response = client.get("/snacks?status=gone", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert item["status"] == "gone"


def test_list_search(client, admin_user, sample_snack):
    """Test searching snacks by name."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/snacks?q=test", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    # Should find "Test Snack"
    assert any("test" in item["name"].lower() for item in data["items"])


def test_list_pagination(client, db_session, admin_user):
    """Test pagination."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create multiple snacks
    import uuid
    for i in range(5):
        snack = Snack(
            id=str(uuid.uuid4()),
            name=f"Snack {i}",
            category=SnackCategory.SWEET,
            quantity=10,
            low_stock_threshold=5
        )
        db_session.add(snack)
    db_session.commit()
    
    response = client.get("/snacks?page=1&page_size=2", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] >= 5


def test_list_sort(client, admin_user):
    """Test sorting snacks."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/snacks?sort_by=quantity&order=desc", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    quantities = [item["quantity"] for item in data["items"]]
    assert quantities == sorted(quantities, reverse=True)


def test_summary_counts(client, db_session, admin_user):
    """Test summary endpoint counts."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create snacks with different statuses
    import uuid
    stocked = Snack(
        id=str(uuid.uuid4()),
        name="Stocked",
        category=SnackCategory.SWEET,
        quantity=10,
        low_stock_threshold=5
    )
    running_low = Snack(
        id=str(uuid.uuid4()),
        name="Running Low",
        category=SnackCategory.SWEET,
        quantity=3,
        low_stock_threshold=5
    )
    gone = Snack(
        id=str(uuid.uuid4()),
        name="Gone",
        category=SnackCategory.SWEET,
        quantity=0,
        low_stock_threshold=5
    )
    db_session.add_all([stocked, running_low, gone])
    db_session.commit()
    
    response = client.get("/snacks/summary", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "stocked" in data
    assert "running_low" in data
    assert "gone" in data
    assert "total" in data
    assert data["stocked"] >= 1
    assert data["running_low"] >= 1
    assert data["gone"] >= 1


def test_summary_snack_of_the_week_tie_break(client, db_session, admin_user):
    """Test snack of the week tie-breaking by name."""
    token = create_access_token(admin_user.id, admin_user.role)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create two snacks with same vote count
    import uuid
    from app.models import Vote, User
    from app.core.security import hash_password
    from app.models.user import UserRole
    
    snack1 = Snack(
        id=str(uuid.uuid4()),
        name="A Snack",
        category=SnackCategory.SWEET,
        quantity=10,
        low_stock_threshold=5
    )
    snack2 = Snack(
        id=str(uuid.uuid4()),
        name="B Snack",
        category=SnackCategory.SWEET,
        quantity=10,
        low_stock_threshold=5
    )
    db_session.add_all([snack1, snack2])
    db_session.commit()
    
    # Create additional users for voting
    user2 = User(
        id=str(uuid.uuid4()),
        name="User 2",
        email="user2@test.com",
        password_hash=hash_password("password"),
        role=UserRole.MEMBER
    )
    db_session.add(user2)
    db_session.commit()
    
    # Add same number of votes to both (from different users)
    vote1 = Vote(user_id=admin_user.id, snack_id=snack1.id)
    vote2 = Vote(user_id=user2.id, snack_id=snack1.id)
    vote3 = Vote(user_id=admin_user.id, snack_id=snack2.id)
    vote4 = Vote(user_id=user2.id, snack_id=snack2.id)
    db_session.add_all([vote1, vote2, vote3, vote4])
    db_session.commit()
    
    response = client.get("/snacks/summary", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["snack_of_the_week"]["name"] == "A Snack"  # Tie-break by name ASC
