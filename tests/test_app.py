from fastapi import HTTPException


async def test_get_empty_applications(client):
    """Test GET applications when database is empty"""
    response = client.get("/applications")
    assert response.status_code == 404
    assert response.json()["detail"] == "Failed to fetch applications from Database"


async def test_get_application_by_username(client, test_application_data):
    """Test retrieving application by username"""
    # Create application first
    create_response = client.post("/applications", json=test_application_data)
    assert create_response.status_code == 201

    # Get application by username
    response = client.get(f"/applications/user/{test_application_data['username']}")
    assert response.status_code == 200
    applications = response.json()
    assert len(applications) == 1
    assert applications[0]["username"] == test_application_data["username"]


async def test_get_all_applications(client, test_application_data):
    """Test retrieving all applications"""
    # Create application first
    create_response = client.post("/applications", json=test_application_data)
    assert create_response.status_code == 201

    # Get all applications
    response = client.get("/applications")
    assert response.status_code == 200
    applications = response.json()
    assert len(applications) == 1
    assert applications[0]["username"] == test_application_data["username"]

async def test_get_nonexistent_username(client):
    """Test retrieving application for non-existent username"""
    response = client.get("/applications/user/nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()