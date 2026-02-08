"""
Test script to verify the complete flow from signup to task creation
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_complete_flow():
    print("Testing complete flow from signup to task creation...")

    # Step 1: Register a new user
    print("\n1. Testing user registration...")
    email = f"testuser_{int(time.time())}@example.com"
    password = "securepassword123"

    register_response = requests.post(
        f"{BASE_URL}/api/register",
        headers={"Content-Type": "application/json"},
        json={"email": email, "password": password}
    )

    if register_response.status_code == 200:
        print("[SUCCESS] Registration successful")
    else:
        print(f"[ERROR] Registration failed: {register_response.text}")
        return False

    # Step 2: Login to get tokens
    print("\n2. Testing login to get tokens...")
    login_response = requests.post(
        f"{BASE_URL}/api/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": email, "password": password}
    )

    if login_response.status_code == 200:
        print("[SUCCESS] Login successful")
        login_data = login_response.json()
        access_token = login_data.get("access_token")
        refresh_token = login_data.get("refresh_token")
    else:
        print(f"[ERROR] Login failed: {login_response.text}")
        return False

    # Step 3: Create a new task
    print("\n3. Testing task creation...")
    headers = {"Authorization": f"Bearer {access_token}"}
    todo_data = {
        "title": "Test task from API flow",
        "description": "This is a test task created via the API"
    }

    create_todo_response = requests.post(
        f"{BASE_URL}/api/todos",
        headers=headers,
        json=todo_data
    )

    if create_todo_response.status_code == 200:
        print("[SUCCESS] Task creation successful")
        todo_data = create_todo_response.json()
        todo_id = todo_data.get("id")
        print(f"  Created task with ID: {todo_id}")
    else:
        print(f"[ERROR] Task creation failed: {create_todo_response.text}")
        return False

    # Step 4: Get all tasks to verify the task was created
    print("\n4. Testing task retrieval...")
    get_todos_response = requests.get(
        f"{BASE_URL}/api/todos",
        headers=headers
    )

    if get_todos_response.status_code == 200:
        todos = get_todos_response.json()
        print(f"[SUCCESS] Retrieved {len(todos)} tasks")
        if any(todo.get("id") == todo_id for todo in todos):
            print("[SUCCESS] Newly created task found in the list")
        else:
            print("[ERROR] Newly created task not found in the list")
            return False
    else:
        print(f"[ERROR] Task retrieval failed: {get_todos_response.text}")
        return False

    # Step 5: Toggle task completion
    print("\n5. Testing task completion toggle...")
    toggle_response = requests.patch(
        f"{BASE_URL}/api/todos/{todo_id}/complete",
        headers=headers
    )

    if toggle_response.status_code == 200:
        toggled_todo = toggle_response.json()
        print(f"[SUCCESS] Task completion toggled. Completed: {toggled_todo.get('completed')}")
    else:
        print(f"[ERROR] Task completion toggle failed: {toggle_response.text}")
        return False

    # Step 6: Delete the test task
    print("\n6. Testing task deletion...")
    delete_response = requests.delete(
        f"{BASE_URL}/api/todos/{todo_id}",
        headers=headers
    )

    if delete_response.status_code == 200:
        print("[SUCCESS] Task deletion successful")
    else:
        print(f"[ERROR] Task deletion failed: {delete_response.text}")
        return False

    print("\n[SUCCESS] All tests passed! The complete flow from signup to task creation works correctly.")
    return True

if __name__ == "__main__":
    test_complete_flow()