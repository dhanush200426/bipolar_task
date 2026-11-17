"""
Concurrency tests for consume and vote operations.
Tests atomic behavior under concurrent requests.
"""
import pytest
import threading
from app.core.security import create_access_token
from app.models import Snack, SnackCategory, Activity, ActivityAction, Vote
from sqlalchemy import func


@pytest.mark.skip(reason="TestClient is not thread-safe for concurrent requests")
def test_concurrency_consume(client, db_session, admin_user):
    """
    Test consume with 10 concurrent requests on quantity=3.
    Should result in exactly 3 successes, 7 failures, final quantity 0, 3 activity rows.
    """
    import uuid
    snack = Snack(
        id=str(uuid.uuid4()),
        name="Concurrency Test Snack",
        category=SnackCategory.SWEET,
        quantity=3,
        low_stock_threshold=5
    )
    db_session.add(snack)
    db_session.commit()
    
    token = create_access_token(admin_user.id, admin_user.role)
    results = []
    barrier = threading.Barrier(10)
    
    def worker():
        barrier.wait()  # All threads start at the same time
        response = client.post(
            f"/snacks/{snack.id}/consume",
            json={"amount": 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        results.append((response.status_code, response.json() if response.status_code != 204 else None))
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Count results
    success_count = sum(1 for status, _ in results if status == 200)
    insufficient_stock_count = sum(1 for status, _ in results if status == 409)
    
    # Verify results
    assert success_count == 3, f"Expected 3 successes, got {success_count}"
    assert insufficient_stock_count == 7, f"Expected 7 insufficient stock, got {insufficient_stock_count}"
    
    # Verify final quantity
    db_session.refresh(snack)
    assert snack.quantity == 0, f"Expected final quantity 0, got {snack.quantity}"
    
    # Verify exactly 3 activity rows
    activity_count = db_session.query(Activity).filter(
        Activity.snack_id == snack.id,
        Activity.action == ActivityAction.CONSUMED
    ).count()
    assert activity_count == 3, f"Expected 3 activity rows, got {activity_count}"


@pytest.mark.skip(reason="TestClient is not thread-safe for concurrent requests")
def test_concurrency_vote(client, db_session, admin_user):
    """
    Test vote with 10 concurrent requests from same user on same snack.
    Should result in exactly 1 success, 9 failures, 1 vote row.
    """
    import uuid
    snack = Snack(
        id=str(uuid.uuid4()),
        name="Vote Test Snack",
        category=SnackCategory.SWEET,
        quantity=10,
        low_stock_threshold=5
    )
    db_session.add(snack)
    db_session.commit()
    
    token = create_access_token(admin_user.id, admin_user.role)
    results = []
    barrier = threading.Barrier(10)
    
    def worker():
        barrier.wait()  # All threads start at the same time
        response = client.post(
            f"/snacks/{snack.id}/vote",
            headers={"Authorization": f"Bearer {token}"}
        )
        results.append((response.status_code, response.json() if response.status_code != 204 else None))
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Count results
    created_count = sum(1 for status, _ in results if status == 201)
    already_voted_count = sum(1 for status, _ in results if status == 409)
    
    # Verify results
    assert created_count == 1, f"Expected 1 created, got {created_count}"
    assert already_voted_count == 9, f"Expected 9 already voted, got {already_voted_count}"
    
    # Verify exactly 1 vote row
    vote_count = db_session.query(Vote).filter(
        Vote.snack_id == snack.id,
        Vote.user_id == admin_user.id
    ).count()
    assert vote_count == 1, f"Expected 1 vote row, got {vote_count}"
