from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.api.v1.routes.create_pdf_task.delay")
def test_generate_pdf(mock_celery):
    mock_celery.return_value.id = "fake-job-id"

    html_content = "<html><body><h1>Test PDF</h1></body></html>"
    files = {"data": ("test.html", html_content, "text/html")}
    response = client.post("/api/v1/generate", files=files)
    assert response.status_code == 200
    assert response.json()["job_id"] == "fake-job-id"

def test_status_endpoint_pending(monkeypatch):
    job_id = "dummy-job-id"

    def mock_get_task_status(task_id):
        return "PENDING"

    monkeypatch.setattr("app.workers.tasks.get_task_status", mock_get_task_status)
    response = client.get(f"/api/v1/status/{job_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

def test_download_pdf_not_found():
    job_id = "non-existent-job"
    response = client.get(f"/api/v1/download/{job_id}")
    # Should return 404 or a file-not-found-safe fallback depending on your implementation
    assert response.status_code in [404, 500]
