from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os, shutil, uuid
from app import models, auth, utils
from app.database import SessionLocal
from fastapi.responses import FileResponse

router = APIRouter(tags=["Files"])

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = ["docx", "pptx", "xlsx"]

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    current_user=Depends(auth.require_role("ops")),
    db: Session = Depends(auth.get_db)
):
    ext = file.filename.split('.')[-1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, detail="Invalid file type")

    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.File(
        filename=file.filename,
        filepath=file_path,
        uploaded_by=current_user.id
    )
    db.add(new_file)
    db.commit()
    return {"message": "File uploaded successfully"}

@router.get("/files")
def list_files(current_user=Depends(auth.require_role("client")), db: Session = Depends(auth.get_db)):
    files = db.query(models.File).all()
    return [{"id": f.id, "filename": f.filename, "uploaded_at": f.uploaded_at} for f in files]

@router.get("/download-file/{file_id}")
def get_download_url(file_id: int, current_user=Depends(auth.require_role("client")), db: Session = Depends(auth.get_db)):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(404, detail="File not found")

    download_token = utils.create_access_token({"file_id": file.id, "user_id": current_user.id})
    return {
        "download_link": f"http://localhost:8000/secure-download/{download_token}",
        "message": "success"
    }

@router.get("/secure-download/{token}")
def secure_download(token: str, db: Session = Depends(auth.get_db), user=Depends(auth.get_current_user)):
    try:
        payload = utils.decode_token(token)
        file_id = payload.get("file_id")
        user_id = payload.get("user_id")
        if user.id != user_id or user.role != "client":
            raise HTTPException(403, detail="Unauthorized")
        file = db.query(models.File).filter(models.File.id == file_id).first()
        if not file:
            raise HTTPException(404, detail="File not found")
        return FileResponse(file.filepath, media_type='application/octet-stream', filename=file.filename)
    except:
        raise HTTPException(403, detail="Invalid or expired link")
