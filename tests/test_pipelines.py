from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pipeline import Pipeline

def create_project(
    client: TestClient,
) -> int:
    response = client.post(
        "/projects",
        json={
            "name": "Pipeline Test Project",
            "description": "Project used in pipeline tests",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_pipeline(
    client: TestClient,
    project_id: int,
) -> dict:
    response = client.post(
        f"/projects/{project_id}/pipelines",
        json={
            "name": "Test Pipeline",
            "description": "Pipeline created by pytest",
        },
    )

    assert response.status_code == 201

    return response.json()

def test_create_pipeline(
        client: TestClient,
):
    project_id = create_project(client)

    response = client.post(
        f"/projects/{project_id}/pipelines",
        json={
            "name": "Daily Sales Pipeline",
            "description": "Processes sales data",
        },
    )

    assert response.status_code ==201

    data= response.json()

    assert data["project_id"] == project_id
    assert data["name"] == "Daily Sales Pipeline"
    assert data["description"] == "Processes sales data"
    assert data["status"] == "draft"
    assert isinstance(data["id"], int)
    assert data["created_at"] is not None

def test_list_pipelines(
        client: TestClinet,
    ):
        project_id = create_project(client)

        create_pipeline(
            client,
            project_id,
        )

        client.post(
            f"/projects/{project_id}/pipelines",
            json={
                 "name": "Second Pipeline",
                "description": "Another pipeline",
            },
        )

        response = client.get(
            f"/projects/{project_id}/pipelines"
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2
        assert data[0]["name"] == "Test Pipeline"
        assert data[1]["name"] == "Second Pipeline"

def test_get_pipeline(
        client: TestClient
    ):
        project_id = create_project(client)

        pipeline = create_pipeline(
            client, 
            project_id,
        )

        response = client.get(
            f"/projects/{project_id}/pipelines/{pipeline["id"]}"
        )

        assert response.status_code ==200
        data = response.json()

        assert data["id"]==pipeline["id"]
        assert data["project_id"]==project_id
        assert data["name"]== "Test Pipeline"


def test_get_nonexistent_pipeline(
    client: TestClient,
):
    project_id = create_project(client)

    response = client.get(
        f"/projects/{project_id}/pipelines/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Pipeline not found"
    }

def test_create_pipeline_for_nonexistent_project(
    client: TestClient,
):
    response = client.post(
        "/projects/999999/pipelines",
        json={
            "name": "Bad Pipeline",
            "description": "Should not exist",
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Project not found"
    }


def test_update_pipeline(
    client: TestClient,
):
    project_id = create_project(client)

    pipeline = create_pipeline(
        client,
        project_id,
    )

    response = client.patch(
        f"/projects/{project_id}/pipelines/{pipeline['id']}",
        json={
            "name": "Updated Pipeline",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Pipeline"
    assert data["description"] == "Pipeline created by pytest"
    assert data["status"] == "draft"

def test_update_pipeline_status(
    client: TestClient,
):
    project_id = create_project(client)

    pipeline = create_pipeline(
        client,
        project_id,
    )

    response = client.patch(
        f"/projects/{project_id}/pipelines/{pipeline['id']}",
        json={
            "status": "active",
        },
    )

    assert response.status_code == 200

    assert response.json()["status"] == "active"


def test_update_pipeline_with_invalid_status(
    client: TestClient,
):
    project_id = create_project(client)

    pipeline = create_pipeline(
        client,
        project_id,
    )

    response = client.patch(
        f"/projects/{project_id}/pipelines/{pipeline['id']}",
        json={
            "status": "running",
        },
    )

    assert response.status_code == 422

def test_delete_pipeline(
    client: TestClient,
):
    project_id = create_project(client)

    pipeline = create_pipeline(
        client,
        project_id,
    )

    response = client.delete(
        f"/projects/{project_id}/pipelines/{pipeline['id']}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/projects/{project_id}/pipelines/{pipeline['id']}"
    )

    assert get_response.status_code == 404

def test_delete_project_removes_its_pipelines(
    client: TestClient,
    db_session: Session,
):
    project_id = create_project(client)

    pipeline = create_pipeline(
        client,
        project_id,
    )

    response = client.delete(
        f"/projects/{project_id}"
    )

    assert response.status_code == 204

    statement = select(Pipeline).where(
        Pipeline.id == pipeline["id"]
    )

    deleted_pipeline = db_session.scalar(
        statement
    )

    assert deleted_pipeline is None