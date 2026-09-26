from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_source import DataSource


def create_project(client: TestClient) -> int:
    response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Project for data source tests",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]

def create_data_source(
    client: TestClient,
    project_id: int,
) -> dict:
    response = client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name": "Test Source",
            "source_type": "csv",
            "config": {
                "path": "/data/test.csv",
            },
        },
    )

    assert response.status_code == 201

    return response.json()

def test_create_data_source(client: TestClient):
    project_id = create_project(client)

    response = client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name": "Sales CSV",
            "source_type": "csv",
            "config": {
                "path": "/data/sales.csv",
            },
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["project_id"] == project_id
    assert data["name"] == "Sales CSV"
    assert data["source_type"] == "csv"
    assert isinstance(data["id"], int)
    assert data["created_at"] is not None


def test_list_data_sources(client: TestClient):
    project_id = create_project(client)

    client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name": "CSV Source",
            "source_type": "csv",
            "config": {
                "path": "/data/file.csv",
            },
        },
    )

    client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name": "API Source",
            "source_type": "api",
            "config": {
                "url": "https://example.com/data",
                "method": "GET",
            },
        },
    )

    response = client.get(
        f"/projects/{project_id}/data-sources"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "CSV Source"
    assert data[1]["name"] == "API Source"


def test_create_data_source_with_invalid_type(
    client: TestClient,
):
    project_id = create_project(client)

    response = client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name": "Broken Source",
            "source_type": "excel-super-duper",
        },
    )

    assert response.status_code == 422


def test_get_data_source(client: TestClient):
    project_id = create_project(client)
    data_source = create_data_source(client, project_id)

    response = client.get(
        f"/projects/{project_id}/data-sources/{data_source['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == data_source["id"]
    assert data["project_id"] == project_id
    assert data["name"] == "Test Source"
    assert data["source_type"] == "csv"


def test_get_nonexistent_data_source(client: TestClient):
    project_id = create_project(client)

    response = client.get(
        f"/projects/{project_id}/data-sources/999999"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Data source not found"
    }

def test_create_data_source_for_nonexistent_project(
    client: TestClient,
):
    response = client.post(
        "/projects/999999/data-sources",
        json={
            "name": "Test Source",
            "source_type": "csv",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Project not found"
    }

def test_update_data_source(client: TestClient):
    project_id = create_project(client)
    data_source = create_data_source(client, project_id)

    response = client.patch(
        f"/projects/{project_id}/data-sources/{data_source['id']}",
        json={
            "name": "Updated Source",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Source"
    assert data["source_type"] == "csv"


def test_delete_data_source(client: TestClient):
    project_id = create_project(client)
    data_source = create_data_source(client, project_id)

    response = client.delete(
        f"/projects/{project_id}/data-sources/{data_source['id']}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/projects/{project_id}/data-sources/{data_source['id']}"
    )


    assert get_response.status_code == 404


def test_delete_project_removes_its_data_sources(
    client: TestClient,
    db_session: Session,
):
    project_id = create_project(client)
    data_source = create_data_source(client, project_id)

    response = client.delete(f"/projects/{project_id}")

    assert response.status_code == 204

    statement = select(DataSource).where(
        DataSource.id == data_source["id"]
    )

    deleted_data_source = db_session.scalar(statement)

    assert deleted_data_source is None

def test_list_projects(client: TestClient):
    client.post(
        "/projects",
        json={
            "name": "Project One",
            "description": "First project",
        },
    )

    client.post(
        "/projects",
        json={
            "name": "Project Two",
            "description": "Second project",
        },
    )

    response = client.get("/projects")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Project One"
    assert data[1]["name"] == "Project Two"


def test_create_data_source_with_config(client : TestClient):
    project_id = create_project(client)

    response = client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name":"Sales CSV",
            "source_type":"csv",
            "config": {
                "path": "/data/sales.csv",
                "delimiter":",",
                "encoding":"utf-8",
            },
        },
    )

    assert response.status_code ==201

    data = response.json()

    assert data["config"]["path"]=="/data/sales.csv"
    assert data["config"]["delimiter"] == ","
    assert data["config"]["encoding"]=='utf-8'

def test_update_data_source_config(client : TestClient):
    project_id= create_project(client)
    data_source = create_data_source(client, project_id)

    response =  client.patch(
        f"/projects/{project_id}/data-sources/{data_source["id"]}",
        json ={
            "config": {
                "path" : "/data/updated.csv"
            }
        },
    )

    assert response.status_code ==200
    assert response.json()["config"] == {
        "path" : "/data/updated.csv"
    }

def test_csv_source_rejects_invalid_config(
        client : TestClient,
):

    project_id = create_project(client)

    response = client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name":"Bad CSV",
            "source_type":"csv",
            "config":{
                "host":"localhost",
                "port":5432,
            },
        },
    )
    assert response.status_code==422


def test_api_source_accepts_api_config(
        client:TestClient,

):
    project_id=create_project(client)
    response = client.post(
        f"/projects/{project_id}/data-sources",
        json={
            "name": "Currency API",
            "source_type": "api",
            "config": {
                "url": "https://example.com/rates",
                "method": "GET",
            },
        },
    )

    assert response.status_code ==201
    data = response.json()

    assert data["source_type"] == "api"
    assert data["config"]["url"] == "https://example.com/rates"
    assert data["config"]["method"] == "GET"

def test_change_type_requires_new_config(
        client : TestClient,

):
    project_id =create_project(client)
    data_source = create_data_source(
        client,
        project_id,
    )

    response = client.patch(
        f"/projects/{project_id}/data-sources/{data_source["id"]}",
        json={
            "source_type":"api",
        },
    )

    assert response.status_code == 422

    assert response.json() == {
       "detail": "Changing source type requires a new config"
    }

def test_change_csv_source_to_api(
    client: TestClient,
):
    project_id=create_project(client)
    data_source=create_data_source(
        client,
        project_id,
    )

    response =client.patch(
        f"/projects/{project_id}/data-sources/{data_source["id"]}",
        json={
            "source_type":"api",
            "config" : {
                "url" : "https://example.com/data",
                "method": "GET",
            },
        },
    )

    assert response.status_code == 200

    data= response.json()

    assert data["source_type"] =="api"
    assert data["config"]["url"]=="https://example.com/data"
    assert data["config"]["method"]=="GET"

def test_update_data_source_rejects_invalid_config(
    client: TestClient,
):
    project_id=create_project(client)
    data_source=create_data_source(
        client,
        project_id,
    )

    response =client.patch(
        f"/projects/{project_id}/data-sources/{data_source["id"]}",
        json={
            "config":{
                "host": "localhost",
            },
        },
    )

    assert response.status_code ==422