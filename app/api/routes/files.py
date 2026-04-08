import os
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file.filename


@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    filename = save_file(file)
    return {"url": f"http://localhost:8000/uploads/{filename}"}


@router.post("/upload/video")
async def upload_video(file: UploadFile = File(...)):
    filename = save_file(file)
    return {"url": f"http://localhost:8000/uploads/{filename}"}


@router.post("/upload/file")
async def upload_any(file: UploadFile = File(...)):
    filename = save_file(file)
    return {"url": f"http://localhost:8000/uploads/{filename}"}
