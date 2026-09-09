"""Document upload, validation, and OCR extraction service."""
import os
import uuid
import hashlib
import json
from typing import List, Tuple
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.config import settings
from app.models.document import UserDocument
from app.schemas.document import DocumentUploadResponse, DocumentExtractResponse, ExtractedField, DocumentOut
from app.utils.exceptions import InvalidInputException, NotFoundException

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"application/pdf", "image/jpeg", "image/png"}


class DocumentService:
    @staticmethod
    def _ensure_upload_dir():
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    @classmethod
    async def upload_document(
        cls,
        db: Session,
        file: UploadFile,
        document_type: str,
        user_id: str = None
    ) -> DocumentUploadResponse:
        cls._ensure_upload_dir()

        # 1. Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise InvalidInputException(
                f"File type '{ext}' is not allowed. Supported formats: PDF, JPG, PNG.",
                details={"allowed_extensions": list(ALLOWED_EXTENSIONS)}
            )

        # 2. Read and validate size
        content = await file.read()
        file_size = len(content)
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise InvalidInputException(
                f"File size exceeds limit of {settings.MAX_UPLOAD_SIZE_MB}MB.",
                details={"max_size_mb": settings.MAX_UPLOAD_SIZE_MB, "file_size_bytes": file_size}
            )

        # 3. Checksum & secure storage key
        checksum = hashlib.sha256(content).hexdigest()
        secure_filename = f"{uuid.uuid4().hex}{ext}"
        storage_path = os.path.join(settings.UPLOAD_DIR, secure_filename)

        with open(storage_path, "wb") as f:
            f.write(content)

        doc = UserDocument(
            user_id=user_id,
            document_type=document_type.upper(),
            original_filename=file.filename,
            storage_key=secure_filename,
            mime_type=file.content_type or "application/octet-stream",
            file_size_bytes=file_size,
            checksum=checksum,
            ocr_status="UPLOADED",
            document_status="NEEDS_REVIEW"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return DocumentUploadResponse(
            document_id=doc.id,
            filename=doc.original_filename,
            document_type=doc.document_type,
            file_size_bytes=doc.file_size_bytes,
            status=doc.ocr_status
        )

    @classmethod
    def extract_document_fields(cls, db: Session, document_id: str) -> DocumentExtractResponse:
        doc = db.query(UserDocument).filter(UserDocument.id == document_id).first()
        if not doc:
            raise NotFoundException(resource="Document", identifier=document_id)

        # Extracted fields based on document type (Grounded OCR simulation)
        dtype = doc.document_type.upper()
        extracted: List[ExtractedField] = []
        preview = ""

        if "INCOME" in dtype:
            extracted = [
                ExtractedField(
                    name="annual_family_income",
                    value=250000,
                    confidence=0.94,
                    requires_confirmation=True,
                    suggested_attribute_key="annual_family_income"
                ),
                ExtractedField(
                    name="issuing_tehsil",
                    value="Bijnor",
                    confidence=0.88,
                    requires_confirmation=True,
                    suggested_attribute_key="district"
                ),
                ExtractedField(
                    name="state",
                    value="Uttar Pradesh",
                    confidence=0.96,
                    requires_confirmation=True,
                    suggested_attribute_key="state"
                )
            ]
            preview = "Government of Uttar Pradesh - Office of Tehsildar. Annual Income certified: Rs 2,50,000."
        elif "CASTE" in dtype:
            extracted = [
                ExtractedField(
                    name="caste_category",
                    value="SC",
                    confidence=0.98,
                    requires_confirmation=True,
                    suggested_attribute_key="caste_category"
                ),
                ExtractedField(
                    name="sub_caste",
                    value="Jatav",
                    confidence=0.91,
                    requires_confirmation=True,
                    suggested_attribute_key="sub_caste"
                )
            ]
            preview = "Scheduled Caste Certificate. Category: SC verified under Presidential Order."
        elif "PROJECT" in dtype or "BUSINESS" in dtype:
            extracted = [
                ExtractedField(
                    name="project_cost",
                    value=300000,
                    confidence=0.92,
                    requires_confirmation=True,
                    suggested_attribute_key="project_cost"
                ),
                ExtractedField(
                    name="business_type",
                    value="tailoring",
                    confidence=0.89,
                    requires_confirmation=True,
                    suggested_attribute_key="business_type"
                )
            ]
            preview = "Micro Enterprise Project Appraisal: Garment Manufacturing / Tailoring Unit."
        else:
            extracted = [
                ExtractedField(
                    name="document_reference_number",
                    value="DOC-2026-9812",
                    confidence=0.85,
                    requires_confirmation=True
                )
            ]
            preview = "Official Document Uploaded. Text recognized."

        doc.ocr_status = "EXTRACTED"
        doc.extracted_data_json = json.dumps([f.model_dump() for f in extracted])
        db.commit()

        return DocumentExtractResponse(
            document_id=doc.id,
            document_type=doc.document_type,
            status=doc.ocr_status,
            fields=extracted,
            raw_text_preview=preview
        )

    @classmethod
    def get_user_documents(cls, db: Session, user_id: str = None) -> List[DocumentOut]:
        query = db.query(UserDocument)
        if user_id:
            query = query.filter(UserDocument.user_id == user_id)
        docs = query.order_by(UserDocument.created_at.desc()).all()
        return [DocumentOut.model_validate(d) for d in docs]
