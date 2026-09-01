from fastapi.testclient import TestClient
import app
from app.main import app

client = TestClient(app)

def test_create_project_with_too_short_name():
    response = client.post(
        "/projects",
        json={
            "name":"a",
            "description":"Invalid Project",
        },
    )


    assert response.status_code == 422