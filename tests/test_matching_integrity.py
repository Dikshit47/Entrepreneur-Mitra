"""Tests for Deterministic Matching Integrity and Ineligibility Capping."""
import pytest


def test_ineligible_profile_capped_score(client):
    # Create profile that violates NBCFDC income threshold (> Rs. 3,00,000)
    prof_res = client.post("/api/v1/profiles", json={
        "language": "en",
        "attributes": {
            "business_type": "tailoring",
            "project_cost": 300000,
            "annual_family_income": 800000,  # Fails <= 300000 limit
            "caste_category": "OBC",
            "state": "Uttar Pradesh",
            "district": "Bijnor"
        }
    })
    profile_id = prof_res.json()["data"]["profile_id"]

    match_res = client.get(f"/api/v1/matching/results?profile_id={profile_id}&lang=en")
    assert match_res.status_code == 200
    results = match_res.json()["data"]["results"]

    nbcfdc_match = next((m for m in results if m["scheme_id"] == "NBCFDC-GTL-001"), None)
    assert nbcfdc_match is not None
    # Mandatory rule failed -> status MUST be NOT_ELIGIBLE
    assert nbcfdc_match["status"] == "NOT_ELIGIBLE"
    # An ineligible scheme MUST NEVER show high confidence score
    assert nbcfdc_match["match_score"] <= 30
    assert nbcfdc_match["score_breakdown"]["eligibility_completeness"] == 15.0


def test_genuine_score_breakdown_consistency(client):
    prof_res = client.post("/api/v1/profiles", json={
        "language": "en",
        "attributes": {
            "business_type": "tailoring",
            "project_cost": 500000,
            "annual_family_income": 180000,
            "caste_category": "OBC",
            "state": "Uttar Pradesh",
            "district": "Bijnor"
        }
    })
    profile_id = prof_res.json()["data"]["profile_id"]

    match_res = client.get(f"/api/v1/matching/results?profile_id={profile_id}&lang=en")
    assert match_res.status_code == 200
    top_match = match_res.json()["data"]["results"][0]

    bd = top_match["score_breakdown"]
    # Verify exact weighted calculation
    recalculated = int(
        (bd["eligibility_completeness"] * 0.35) +
        (bd["purpose_fit"] * 0.25) +
        (bd["financial_fit"] * 0.15) +
        (bd["geography_fit"] * 0.10) +
        (bd["document_readiness"] * 0.10) +
        (bd["user_preference"] * 0.05)
    )
    assert abs(top_match["match_score"] - recalculated) <= 1
