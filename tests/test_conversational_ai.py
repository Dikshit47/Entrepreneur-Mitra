"r""Comprehensive tests for enhanced conversational AI engine and DigiLocker modal resilience."""
from app.services.interview_service import InterviewService
from app.schemas.interview import InterviewTurnRequest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_scheme_inquiry_no_false_sc_extraction():
    """Ensure inquiry with 'scheme' does not trigger false positive SC caste category."""
    req = InterviewTurnRequest(text="Konsi scheme mere liye sabse acchi hai?", language="hinglish")
    res = InterviewService.process_turn(req, {})
    assert "caste_category" not in res.extracted_attributes
    assert "NBCFDC" in res.assistant_message or "Swarnima" in res.assistant_message


def test_interest_rate_inquiry_conversational():
    """Ensure interest rate questions get exact MoSJE rates."""
    req = InterviewTurnRequest(text="byaj kitna lagega?", language="hi")
    res = InterviewService.process_turn(req, {})
    assert "4%" in res.assistant_message


def test_document_and_digilocker_inquiry():
    """Ensure inquiries about documents reference DigiLocker and required certificates."""
    req = InterviewTurnRequest(text="What documents are needed?", language="en")
    res = InterviewService.process_turn(req, {})
    assert "DigiLocker" in res.assistant_message
    assert "Caste Certificate" in res.assistant_message or "Income Certificate" in res.assistant_message


def test_greetings_and_name_extraction():
    """Ensure applicant name is cleanly extracted and greeted."""
    req = InterviewTurnRequest(text="Mera naam Priya Sharma hai aur main silai shuru karna chahti hoon", language="hinglish")
    res = InterviewService.process_turn(req, {})
    assert res.extracted_attributes.get("name") == "Priya Sharma"
    assert res.extracted_attributes.get("business_type") == "tailoring"


def test_html_modal_failsafe_attributes():
    """Ensure HTML includes inline failsafe onclick handlers for instant modal close."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "btnDlCloseX" in html
    assert "btnDlCancel" in html
    assert "classList.remove('open')" in html
    assert "digiLockerModal" in html
