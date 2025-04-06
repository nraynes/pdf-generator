from fastapi import APIRouter, UploadFile, File
from app.workers.tasks import create_pdf_task

router = APIRouter()

@router.post("/generate")
async def generate_pdf(data: UploadFile = File(...)):
    job_id = create_pdf_task.delay(data.filename, await data.read())
    return {"job_id": job_id.id}

@router.get("/status/{job_id}")
def check_status(job_id: str):
    from app.workers.tasks import get_task_status
    return {"status": get_task_status(job_id)}

@router.get("/download/{job_id}")
def download_pdf(job_id: str):
    from fastapi.responses import FileResponse
    path = f"generated_pdfs/{job_id}.pdf"
    return FileResponse(path, media_type='application/pdf', filename="document.pdf")