"""Tests for comprehensive, authentic MoSJE and Allied scheme catalog."""
import pytest
from app.database import SessionLocal
from app.models.scheme import Scheme, SchemeRule, SchemeBenefit, DocumentRequirement, SchemeSource


def test_scheme_catalog_count_and_authenticity():
    db = SessionLocal()
    try:
        schemes = db.query(Scheme).all()
        assert len(schemes) >= 11, f"Expected at least 11 schemes, found {len(schemes)}"

        for s in schemes:
            assert s.scheme_id, "Scheme must have an ID"
            assert s.name, f"Scheme {s.scheme_id} missing name"
            assert s.ministry, f"Scheme {s.scheme_id} missing ministry"
            assert s.official_url.startswith("http"), f"Scheme {s.scheme_id} has invalid official URL: {s.official_url}"
            assert s.status == "ACTIVE"

            # Check rules
            rules = db.query(SchemeRule).filter(SchemeRule.scheme_id == s.scheme_id).all()
            assert len(rules) > 0, f"Scheme {s.scheme_id} has no rules"

            # Check benefits
            benefits = db.query(SchemeBenefit).filter(SchemeBenefit.scheme_id == s.scheme_id).all()
            assert len(benefits) > 0, f"Scheme {s.scheme_id} has no benefits"
            for b in benefits:
                assert b.min_value >= 0
                assert b.max_value >= b.min_value
                assert b.interest_rate >= 0

            # Check sources
            sources = db.query(SchemeSource).filter(SchemeSource.scheme_id == s.scheme_id).all()
            assert len(sources) > 0, f"Scheme {s.scheme_id} has no verified sources"
    finally:
        db.close()
