import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Document
from schemas import DocumentResponse
from dependencies import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Upload a document
@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Save the file to disk with a unique name to avoid overwrites
    safe_filename = f"{current_user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata to the database
    new_document = Document(
        filename=file.filename,
        filepath=file_path,
        owner_id=current_user.id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

# List documents — admin sees all, regular user sees only their own
@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "admin":
        return db.query(Document).all()
    return db.query(Document).filter(Document.owner_id == current_user.id).all()

# Delete a document — only the owner or an admin can delete it
@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this document"
        )

    # Delete the physical file from disk
    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    db.delete(document)
    db.commit()
    return {"detail": "Document deleted successfully"}