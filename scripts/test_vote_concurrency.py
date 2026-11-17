"""
Concurrency test for vote endpoint.
Tests that exactly 1 vote succeeds when the same user votes 10 times.
"""
import requests
import threading

BASE_URL = "http://localhost:8000"
EMAIL = "admin@example.com"
PASSWORD = "admin123"

def login():
    """Login and return token."""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": EMAIL,
        "password": PASSWORD
    })
    return response.json()["access_token"]

def create_snack(token, name):
    """Create a snack for testing."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/snacks", json={
        "name": name,
        "category": "sweet",
        "quantity": 10,
        "low_stock_threshold": 5
    }, headers=headers)
    return response.json()["id"]

def vote_snack(snack_id, token, results):
    """Vote for snack and record result."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL}/snacks/{snack_id}/vote", headers=headers)
        results.append((response.status_code, response.json()))
    except Exception as e:
        results.append((0, str(e)))

def main():
    print("=== Vote Concurrency Test ===")
    
    # Login
    token = login()
    print(f"Logged in as {EMAIL}")
    
    # Create snack
    snack_name = "Test Snack Vote"
    snack_id = create_snack(token, snack_name)
    print(f"Created snack '{snack_name}' with ID {snack_id}")
    
    # Fire 10 concurrent vote requests from the same user
    results = []
    threads = []
    barrier = threading.Barrier(10)
    
    def worker():
        barrier.wait()  # All threads start at the same time
        vote_snack(snack_id, token, results)
    
    for _ in range(10):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Count results
    created_count = sum(1 for status, _ in results if status == 201)
    already_voted_count = sum(1 for status, _ in results if status == 409)
    other_count = len(results) - created_count - already_voted_count
    
    print(f"\nResults:")
    print(f"  201 (created): {created_count}")
    print(f"  409 (already voted): {already_voted_count}")
    print(f"  Other: {other_count}")
    
    # Check final vote count
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/snacks/{snack_id}", headers=headers)
    final_vote_count = response.json()["vote_count"]
    print(f"\nFinal vote count: {final_vote_count}")
    
    print(f"\nExpected: 1 x 201, 9 x 409, final vote count 1")
    print(f"Match: {created_count == 1 and already_voted_count == 9 and final_vote_count == 1}")
    
    # Cleanup
    requests.delete(f"{BASE_URL}/snacks/{snack_id}", headers=headers)
    print(f"Cleaned up test snack")

if __name__ == "__main__":
    main()
