"""
Concurrency test for consume endpoint.
Tests that exactly N requests succeed when quantity is N.
"""
import requests
import threading
import time

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

def create_snack(token, name, quantity):
    """Create a snack for testing."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/snacks", json={
        "name": name,
        "category": "sweet",
        "quantity": quantity,
        "low_stock_threshold": 5
    }, headers=headers)
    return response.json()["id"]

def consume_snack(snack_id, token, amount, results):
    """Consume snack and record result."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL}/snacks/{snack_id}/consume", json={
            "amount": amount
        }, headers=headers)
        results.append((response.status_code, response.json()))
    except Exception as e:
        results.append((0, str(e)))

def main():
    print("=== Consume Concurrency Test ===")
    
    # Login
    token = login()
    print(f"Logged in as {EMAIL}")
    
    # Create snack with quantity 3
    snack_name = "Test Snack Concurrency"
    snack_id = create_snack(token, snack_name, 3)
    print(f"Created snack '{snack_name}' with ID {snack_id}, quantity 3")
    
    # Fire 10 concurrent consume requests (amount=1 each)
    results = []
    threads = []
    barrier = threading.Barrier(10)
    
    def worker():
        barrier.wait()  # All threads start at the same time
        consume_snack(snack_id, token, 1, results)
    
    for _ in range(10):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Count results
    success_count = sum(1 for status, _ in results if status == 200)
    insufficient_stock_count = sum(1 for status, _ in results if status == 409)
    other_count = len(results) - success_count - insufficient_stock_count
    
    print(f"\nResults:")
    print(f"  200 (success): {success_count}")
    print(f"  409 (insufficient stock): {insufficient_stock_count}")
    print(f"  Other: {other_count}")
    
    # Check final quantity
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/snacks/{snack_id}", headers=headers)
    final_quantity = response.json()["quantity"]
    print(f"\nFinal quantity: {final_quantity}")
    
    # Check activity count
    # This would require querying activities, skipping for now
    
    print(f"\nExpected: 3 x 200, 7 x 409, final quantity 0")
    print(f"Match: {success_count == 3 and insufficient_stock_count == 7 and final_quantity == 0}")
    
    # Cleanup
    requests.delete(f"{BASE_URL}/snacks/{snack_id}", headers=headers)
    print(f"Cleaned up test snack")

if __name__ == "__main__":
    main()
