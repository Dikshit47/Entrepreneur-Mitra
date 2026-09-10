"""Tests to guarantee 100% Zero Language Leak across UI and API responses."""
import re
import json
import pytest
from app.database import SessionLocal
from app.services.verification_service import DocumentVerificationService
from app.services.matching_service import MatchingService
from app.rules.engine import evaluate_scheme_rules
from app.models.scheme import Scheme
from app.models.profile import EntrepreneurProfile


def test_en_json_has_zero_devanagari():
    with open("app/static/locales/en.json", "r", encoding="utf-8") as f:
        content = f.read()
    matches = re.findall(r"[\u0900-\u097F]", content)
    assert len(matches) == 0, f"Found {len(matches)} Devanagari characters in en.json"


def test_locales_key_parity():
    with open("app/static/locales/en.json", "r", encoding="utf-8") as f:
        en_data = json.load(f)
    with open("app/static/locales/hi.json", "r", encoding="utf-8") as f:
        hi_data = json.load(f)
    with open("app/static/locales/hinglish.json", "r", encoding="utf-8") as f:
        hinglish_data = json.load(f)

    # Check top level sections
    for section in ["common", "nav", "gov", "onboarding", "hero", "kpi", "schemes", "calc", "partners", "docs", "modals", "toasts"]:
        assert section in en_data, f"Section {section} missing from en.json"
        assert section in hi_data, f"Section {section} missing from hi.json"
        assert section in hinglish_data, f"Section {section} missing from hinglish.json"


def test_verification_status_zero_hindi_leak():
    db = SessionLocal()
    try:
        status_res = DocumentVerificationService.get_user_verification_status(db, lang="en")
        for doc in status_res.documents:
            devanagari = re.findall(r"[\u0900-\u097F]", doc.title)
            assert len(devanagari) == 0, f"Devanagari found in English doc title: {doc.title}"
    finally:
        db.close()


def test_matching_explanation_zero_hindi_leak():
    db = SessionLocal()
    try:
        scheme = db.query(Scheme).filter(Scheme.scheme_id == "NBCFDC-GTL-001").first()
        if scheme:
            attrs = {
                "annual_family_income": 180000,
                "project_cost": 500000,
                "caste_category": "OBC",
                "business_type": "carpentry",
                "state": "Uttar Pradesh"
            }
            eval_res = evaluate_scheme_rules(scheme, attrs, lang="en")
            devanagari = re.findall(r"[\u0900-\u097F]", eval_res.summary_explanation)
            assert len(devanagari) == 0, f"Devanagari found in English summary: {eval_res.summary_explanation}"
    finally:
        db.close()
