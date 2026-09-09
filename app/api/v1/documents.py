"""Document upload, validation, and OCR extraction API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_optional_current_user
from app.models.user import User
from app.models.document import UserDocument
from app.schemas.document import DocumentUploadResponse, DocumentExtractResponse, DocumentOut
from app.schemas.common import ApiResponse
from app.services.document_service import DocumentService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=ApiResponse[DocumentUploadResponse])
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(..., description="Document type e.g. INCOME_CERTIFICATE, CASTE_CERTIFICATE, PROJECT_REPORT"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Upload an entrepreneur document securely with mime validation, size check, and checksumming."""
    user_id = current_user.id if current_user else None
    uploaded = await DocumentService.upload_document(db, file, document_type, user_id=user_id)
    return ApiResponse.success_response(uploaded)


@router.post("/{document_id}/extract", response_model=ApiResponse[DocumentExtractResponse])
def extract_document_fields(document_id: str, db: Session = Depends(get_db)):
    """Extract candidate profile fields from the document with confidence scores (requires human confirmation)."""
    extracted = DocumentService.extract_document_fields(db, document_id)
    return ApiResponse.success_response(extracted)


@router.get("", response_model=ApiResponse[List[DocumentOut]])
def list_documents(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """List uploaded documents."""
    user_id = current_user.id if current_user else None
    docs = DocumentService.get_user_documents(db, user_id=user_id)
    return ApiResponse.success_response(docs)


@router.delete("/{document_id}", response_model=ApiResponse[dict])
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete a document."""
    doc = db.query(UserDocument).filter(UserDocument.id == document_id).first()
    if not doc:
        raise NotFoundException(resource="Document", identifier=document_id)
    db.delete(doc)
    db.commit()
    return ApiResponse.success_response({"deleted": True, "document_id": document_id})
