"""Document Management and OCR schemas."""
from typing import List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ExtractedField(BaseModel):
    name: str
    value: Any
    confidence: float
    requires_confirmation: bool = True
    suggested_attribute_key: Optional[str] = None


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    document_type: str
    file_size_bytes: int
    status: str  # UPLOADED, PROCESSING, EXTRACTED


class DocumentExtractResponse(BaseModel):
    document_id: str
    document_type: str
    status: str
    fields: List[ExtractedField]
    raw_text_preview: Optional[str] = None


class DocumentOut(BaseModel):
    id: str
    document_type: str
    original_filename: str
    file_size_bytes: int
    ocr_status: str
    document_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
