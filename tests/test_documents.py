"""Tests for Document Management and Extraction."""
import io


def test_document_upload_and_extraction(client):
    # 1. Upload Income Certificate PDF
    file_content = b"%PDF-1.4 Mock Income Certificate content for Ramesh Kumar"
    file_obj = io.BytesIO(file_content)

    res_upload = client.post(
        "/api/v1/documents",
        files={"file": ("income_cert.pdf", file_obj, "application/pdf")},
        data={"document_type": "INCOME_CERTIFICATE"}
    )
    assert res_upload.status_code == 200
    upload_data = res_upload.json()["data"]
    assert "document_id" in upload_data
    doc_id = upload_data["document_id"]

    # 2. Extract Fields
    res_extract = client.post(f"/api/v1/documents/{doc_id}/extract")
    assert res_extract.status_code == 200
    extract_data = res_extract.json()["data"]
    assert len(extract_data["fields"]) > 0

    income_field = next(f for f in extract_data["fields"] if f["name"] == "annual_family_income")
    assert income_field["value"] == 250000
    assert income_field["requires_confirmation"] is True


def test_document_invalid_extension(client):
    bad_file = io.BytesIO(b"echo 'malicious'")
    res = client.post(
        "/api/v1/documents",
        files={"file": ("script.exe", bad_file, "application/x-msdownload")},
        data={"document_type": "INCOME_CERTIFICATE"}
    )
    assert res.status_code == 422
    assert res.json()["success"] is False
    assert res.json()["error"]["code"] == "INVALID_INPUT"
