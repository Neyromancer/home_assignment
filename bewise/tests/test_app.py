async def test_get_empty_applications(client):
    response = client.get("/applications")
    assert response.status_code == 404
    assert response.json()["detail"] == "Failed to fetch applications from Database"


async def test_get_applications_by_username(client, test_application_data):
    create_response = client.post("/applications", json=test_application_data[0])
    assert create_response.status_code == 201

    response = client.get(f"/applications/{test_application_data[0]['username']}")
    assert response.status_code == 200
    applications = response.json()
    assert len(applications) == 1
    assert applications[0]["username"] == test_application_data[0]["username"]


async def test_get_all_applications(client, test_application_data):
    for test_application in test_application_data:
        create_response = client.post("/applications", json=test_application)
        assert create_response.status_code == 201

    response = client.get("/applications")
    assert response.status_code == 200

    applications = response.json()
    assert len(applications) == 2
    assert applications[0]["username"] == test_application_data[0]["username"]


async def test_get_nonexistent_username(client):
    response = client.get("/applications/user/nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


async def test_application_pagination(client, test_application_data):
    for i in range(20):
        modified_data = test_application_data.copy()
        modified_data[0]["username"] = f"TestUser{i}"
        client.post("/applications", json=modified_data[0])

    response = client.get("/applications")
    assert response.status_code == 200
    assert len(response.json()) == 20

    response = client.get("/applications?page=1&size=10")
    assert response.status_code == 200
    assert len(response.json()) == 10
