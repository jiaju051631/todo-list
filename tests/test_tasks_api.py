from pathlib import Path
import pytest
import sys

top_level_dir = Path(__file__).parent.parent
sys.path.insert(0, str(top_level_dir))

import config

VALID_ACCESS_TOKEN = config.VALID_ACCESS_TOKEN
INVALID_ACCESS_TOKEN = config.INVALID_ACCESS_TOKEN


# Test case 1: Index page
def test_index_page(client):
    response = client.get("/")
    assert "Welcome to Todo-List" in response.text
    assert "Log in with Google" in response.text
    assert "Log in with Github" in response.text
    assert "Log in with Facebook" in response.text


# Test case 2.1: Add a Todo items (invalid access token)
def test_add_task_invalid_token(client, add_and_delete_task):
    task_name = "test_add_task_invalid_token"
    response = client.post(
        f"/task/add/{task_name}", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert "Failed to add the TODO item" in response.text
    assert "Access denied: Invalid access token" in response.text


# Test case 2.2: Add a Todo items (valid access token)
def test_add_task_valied_token(client, add_and_delete_task):
    task_name = "Test TODO item 2"
    response = client.post(
        f"/task/add/{task_name}", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {VALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert "TODO item is successfully added" in response.text


# Test case 3.1: Delete a Todo items (invalid access token)
def test_delete_task_invalid_token(client, add_and_delete_task):
    task_id = 1
    response = client.delete(
        f"/task/delete/{task_id}", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert "Failed to delete the TODO item" in response.text
    assert "Access denied: Invalid access token" in response.text


# Test case 3.2: Delete a Todo items (valid access token)
def test_delete_task_valid_token(client, add_and_delete_task):
    task_id = 1
    response = client.delete(
        f"/task/delete/{task_id}", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {VALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert f"TODO item {task_id} is successfully deleted." == response.text


# Test case 4.1: List all Todo items (invalid access token)
def test_list_task_invalid_token(client, add_and_delete_task):
    response = client.get(
        "/task/list", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert "Failed to list the TODO items" in response.text
    assert "Access denied: Invalid access token" in response.text


# Test case 4.2: List all Todo items (valid access token)
def test_list_task_valid_token(client, add_and_delete_task):
    response = client.get(
        "/task/list", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {VALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert "Task ID: 1" in response.text
    assert "Task name: Test TODO item 1" in response.text
    assert "Completed: False" in response.text


# Test case 5.1: Mark a Todo items as complete (invalid access token)
def test_mark_complete_invalid_token(client, add_and_delete_task):
    task_id = 1
    response = client.put(
        f"/task/mark-complete/{task_id}", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert "Failed to mark the TODO item as complete" in response.text
    assert "Access denied: Invalid access token" in response.text


# Test case 5.2: Mark a Todo items as complete (valid access token)
def test_mark_complete_valid_token(client, add_and_delete_task):
    task_id = 1
    response = client.put(
        f"/task/mark-complete/{task_id}", 
        base_url="https://127.0.0.1:5000",
        headers={"Authorization": f"Bearer {VALID_ACCESS_TOKEN}"}
    )
    assert response.status_code == 200
    assert f"TODO item {task_id} is successfully marked as complete" in response.text