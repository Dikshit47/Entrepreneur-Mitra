"""Standardized application exceptions and error codes."""
from typing import Optional, Any


class AppException(Exception):
    """Base application exception matching Master Blueprint error envelope."""
    def __init__(
        self,
        code: str = "INTERNAL_ERROR",
        message: str = "An unexpected error occurred.",
        user_message: Optional[str] = None,
        status_code: int = 400,
        retryable: bool = False,
        details: Optional[Any] = None
    ):
        self.code = code
        self.message = message
        self.user_message = user_message or message
        self.status_code = status_code
        self.retryable = retryable
        self.details = details
        super().__init__(self.message)


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource", identifier: str = ""):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource} {identifier} not found.",
            user_message=f"Requested {resource.lower()} was not found.",
            status_code=404
        )


class AuthRequiredException(AppException):
    def __init__(self, message: str = "Authentication credentials required."):
        super().__init__(
            code="AUTH_REQUIRED",
            message=message,
            user_message="Kripya login karein (Please log in to continue).",
            status_code=401
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "You do not have permission to access this resource."):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            user_message="Aapko is resource ko access karne ki permission nahi hai.",
            status_code=403
        )


class InvalidInputException(AppException):
    def __init__(self, message: str = "Invalid input data provided.", details: Optional[Any] = None):
        super().__init__(
            code="INVALID_INPUT",
            message=message,
            user_message="Diya gaya data galat ya adhoora hai. Kripya jaanch karein.",
            status_code=422,
            details=details
        )


class ProfileIncompleteException(AppException):
    def __init__(self, missing_fields: Optional[list] = None):
        fields_str = ", ".join(missing_fields) if missing_fields else "required fields"
        super().__init__(
            code="PROFILE_INCOMPLETE",
            message=f"Profile is missing required fields: {fields_str}",
            user_message="Aapki profile mein kuch zaroori jaankari baaki hai.",
            status_code=400,
            details={"missing_fields": missing_fields or []}
        )


class SchemeDataStaleException(AppException):
    def __init__(self, scheme_id: str):
        super().__init__(
            code="SCHEME_DATA_STALE",
            message=f"Scheme data for {scheme_id} requires official re-verification.",
            user_message="Is scheme ki jaankari abhi sarkari portal se verify ki ja rahi hai.",
            status_code=422,
            retryable=False
        )
