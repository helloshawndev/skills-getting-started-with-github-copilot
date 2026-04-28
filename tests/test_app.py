import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange
    # (No special setup needed, use default app state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_prevent_duplicate():
    # Arrange
    activity = "Art Club"
    email = "testuser@mergington.edu"

    # Act
    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Second signup should fail (duplicate)
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_unregister_participant():
    # Arrange
    activity = "Drama Club"
    email = "removeuser@mergington.edu"
    # Sign up first
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Try deleting again (should fail)
    response2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "nouser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
