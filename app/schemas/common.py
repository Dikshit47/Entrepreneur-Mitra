"""Common API response envelopes and meta definitions."""
import uuid
from typing import Generic, TypeVar, Optional, Any, Dict
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class MetaInfo(BaseModel):
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:12]}")
    timestamp: Optional[str] = None


class ErrorDetail(BaseModel):
    code: str
    message: str
    user_message: str
    retryable: bool = False
    details: Optional[Any] = None


class ApiResponse(BaseModel, Generic[DataT]):
    success: bool = True
    data: Optional[DataT] = None
    error: Optional[ErrorDetail] = None
    meta: MetaInfo = Field(default_factory=MetaInfo)

    @classmethod
    def success_response(cls, data: DataT, request_id: Optional[str] = None) -> "ApiResponse[DataT]":
        meta = MetaInfo(request_id=request_id) if request_id else MetaInfo()
        return cls(success=True, data=data, error=None, meta=meta)

    @classmethod
    def error_response(
        cls,
        code: str,
        message: str,
        user_message: Optional[str] = None,
        retryable: bool = False,
        details: Optional[Any] = None,
        request_id: Optional[str] = None
    ) -> "ApiResponse[None]":
        meta = MetaInfo(request_id=request_id) if request_id else MetaInfo()
        err = ErrorDetail(
            code=code,
            message=message,
            user_message=user_message or message,
            retryable=retryable,
            details=details
        )
        return cls(success=False, data=None, error=err, meta=meta)
