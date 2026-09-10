from fastapi.testclient import TestClient


# Test tworzenia projektu
def test_create_project(client: TestClient):
    response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Created by pytest",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Project"
    assert data["description"] == "Created by pytest"
    assert isinstance(data["id"], int)
    assert data["created_at"] is not None


# Test GET po ID
def test_get_project(client: TestClient):
    create_response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Test description",
        },
    )

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == project_id
    assert data["name"] == "Test Project"
    assert data["description"] == "Test description"


# Test GET nieistniejącego projektu
def test_get_nonexistent_project(client: TestClient):
    response = client.get("/projects/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Project not found"
    }


# Test PATCH
def test_update_project(client: TestClient):
    create_response = client.post(
        "/projects",
        json={
            "name": "Old Name",
            "description": "Original description",
        },
    )

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    response = client.patch(
        f"/projects/{project_id}",
        json={
            "name": "Updated Name",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Name"
    assert data["description"] == "Original description"


# Test DELETE
def test_delete_project(client: TestClient):
    create_response = client.post(
        "/projects",
        json={
            "name": "Delete Me",
            "description": "Temporary project",
        },
    )

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/projects/{project_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/projects/{project_id}"
    )

    assert get_response.status_code == 404


# Test walidacji
def test_create_project_with_too_short_name(
    client: TestClient,
):
    response = client.post(
        "/projects",
        json={
            "name": "A",
        },
    )

    assert response.status_code == 422