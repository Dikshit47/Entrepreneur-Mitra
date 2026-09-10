"""Document Management, DigiLocker Verification, and OCR schemas."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


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
    verification_status: str = "UNVERIFIED"
    source: str = "MANUAL_UPLOAD"
    is_sandbox: bool = False


class DocumentExtractResponse(BaseModel):
    document_id: str
    document_type: str
    status: str
    fields: List[ExtractedField]
    raw_text_preview: Optional[str] = None
    trust_level: str = "OCR_EXTRACTION"
    requires_user_confirmation: bool = True


class DigiLockerInitiateRequest(BaseModel):
    document_type: str = Field(..., description="Document to verify: CASTE_CERTIFICATE, INCOME_CERTIFICATE, AADHAAR")
    user_id: Optional[str] = None
    state: Optional[str] = "Uttar Pradesh"


class DigiLockerInitiateResponse(BaseModel):
    session_id: str
    document_type: str
    consent_url: str
    is_sandbox: bool = True
    mode_label: str = "Demo / Sandbox Verification"
    disclaimer: str = "SIH 2026 Evaluation: Simulated DigiLocker Requester Sandbox. Authoritative mock verification without production MeitY credentials."


class DigiLockerVerifyRequest(BaseModel):
    session_id: str
    document_type: str
    user_id: Optional[str] = None
    aadhaar_last4: Optional[str] = "4321"
    citizen_name: Optional[str] = None


class DigiLockerVerifyResponse(BaseModel):
    document_id: str
    document_type: str
    verification_status: str  # DIGILOCKER_VERIFIED, ISSUER_VERIFIED, VERIFICATION_FAILED
    source: str = "DIGILOCKER_ISSUER"
    trust_hierarchy_rank: int = 1  # 1: Issuer-backed DigiLocker, 2: Authoritative, 3: Validated Upload, 4: Manual Review, 5: OCR, 6: User-entered
    trust_level: str = "ISSUER_BACKED_DIGILOCKER"
    issuer: str
    issued_date: str
    verification_reference: str
    is_sandbox: bool = True
    mode_badge: str = "Demo / Sandbox Verification"
    extracted_attributes: Dict[str, Any]
    verified_at: str


class DocumentStatusItem(BaseModel):
    document_type: str
    title: str
    mandatory: bool = True
    status: str  # UNVERIFIED, VERIFICATION_PENDING, DIGILOCKER_VERIFIED, ISSUER_VERIFIED, MANUAL_REVIEW, VERIFICATION_FAILED
    trust_level: str
    source: str
    issuer: Optional[str] = None
    verification_reference: Optional[str] = None
    is_sandbox: bool = False
    verified_at: Optional[str] = None


class DocumentVerificationStatusResponse(BaseModel):
    user_id: Optional[str] = None
    overall_readiness_score: int
    documents: List[DocumentStatusItem]
    trust_hierarchy: List[str] = [
        "1. Issuer-backed DigiLocker verification (Highest Trust)",
        "2. Authoritative department API verification",
        "3. Validated uploaded document (SHA-256 / Format checked)",
        "4. Manual administrative review",
        "5. OCR-only extraction (Requires human confirmation)",
        "6. User-entered self declaration (Lowest Trust)"
    ]


class DocumentOut(BaseModel):
    id: str
    document_type: str
    original_filename: str
    file_size_bytes: int
    ocr_status: str
    document_status: str
    verification_status: Optional[str] = "UNVERIFIED"
    source: Optional[str] = "MANUAL_UPLOAD"
    verification_method: Optional[str] = None
    issuer: Optional[str] = None
    issued_date: Optional[str] = None
    verified_at: Optional[datetime] = None
    verification_reference: Optional[str] = None
    is_sandbox: Optional[bool] = True
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
