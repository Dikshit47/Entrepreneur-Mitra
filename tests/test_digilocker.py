"""Tests for DigiLocker Document Verification and Trust Layer."""
import pytest


def test_digilocker_initiate_sandbox(client):
    res = client.post("/api/v1/documents/digilocker/initiate", json={
        "document_type": "CASTE_CERTIFICATE",
        "state": "Uttar Pradesh"
    })
    assert res.status_code == 200
    data = res.json()["data"]
    assert "session_id" in data
    assert data["is_sandbox"] is True
    assert "Demo / Sandbox Verification" in data["mode_label"]
    assert "Simulated DigiLocker Requester Sandbox" in data["disclaimer"]


def test_digilocker_verify_document(client):
    # 1. Initiate
    init_res = client.post("/api/v1/documents/digilocker/initiate", json={
        "document_type": "INCOME_CERTIFICATE",
        "state": "Uttar Pradesh"
    })
    session_id = init_res.json()["data"]["session_id"]

    # 2. Verify in Sandbox Mode
    verify_res = client.post("/api/v1/documents/digilocker/verify", json={
        "session_id": session_id,
        "document_type": "INCOME_CERTIFICATE",
        "aadhaar_last4": "4321",
        "citizen_name": "Ramesh Kumar"
    })
    assert verify_res.status_code == 200
    v_data = verify_res.json()["data"]

    assert v_data["verification_status"] == "DIGILOCKER_VERIFIED"
    assert v_data["source"] == "DIGILOCKER_ISSUER"
    assert v_data["trust_hierarchy_rank"] == 1
    assert v_data["trust_level"] == "ISSUER_BACKED_DIGILOCKER"
    assert v_data["is_sandbox"] is True
    assert "extracted_attributes" in v_data
    assert v_data["extracted_attributes"]["annual_family_income"] == 180000


def test_document_verification_status_and_readiness(client):
    res = client.get("/api/v1/documents/verification-status")
    assert res.status_code == 200
    data = res.json()["data"]
    assert "overall_readiness_score" in data
    assert "documents" in data
    assert len(data["documents"]) >= 3
    assert "trust_hierarchy" in data
    assert len(data["trust_hierarchy"]) == 6
