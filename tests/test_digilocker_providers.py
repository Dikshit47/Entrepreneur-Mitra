"""Tests for DigiLocker Sandbox vs Production provider isolation."""
import pytest
from app.services.verification_service import (
    DigiLockerSandboxProvider,
    ProductionDigiLockerProvider,
    DocumentVerificationService
)
from app.schemas.document import DigiLockerInitiateRequest
from app.utils.exceptions import InvalidInputException


def test_sandbox_provider_labelling():
    provider = DigiLockerSandboxProvider()
    req = DigiLockerInitiateRequest(document_type="CASTE_CERTIFICATE")
    resp = provider.initiate(req)
    assert resp.is_sandbox is True
    assert "Sandbox" in resp.mode_label
    assert "sandbox.digitallocker.gov.in" in resp.consent_url


def test_production_provider_safe_failure_without_credentials():
    provider = ProductionDigiLockerProvider()
    req = DigiLockerInitiateRequest(document_type="INCOME_CERTIFICATE")
    # Should fail safely if credentials are not configured
    try:
        resp = provider.initiate(req)
        # If credentials were mock configured in env, assert it is production
        assert resp.is_sandbox is False
    except InvalidInputException as e:
        assert "Production DigiLocker credentials" in str(e)
