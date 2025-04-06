from celery import Celery
from app.services.pdf_generator import generate_pdf
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery("worker", broker=redis_url, backend=redis_url)


@celery.task(name="create_pdf_task")
def create_pdf_task(filename: str, content: bytes):
    job_id = create_pdf_task.request.id
    output_path = f"generated_pdfs/{job_id}.pdf"
    os.makedirs("generated_pdfs", exist_ok=True)
    generate_pdf(content, output_path)
    return job_id


def get_task_status(task_id: str):
    result = celery.AsyncResult(task_id)
    return result.status
