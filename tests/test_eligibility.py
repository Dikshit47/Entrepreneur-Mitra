"""Tests for the Deterministic Eligibility Engine."""


def test_eligibility_evaluation_pass(client):
    # Ramesh Persona: eligible for NBCFDC-GTL-001
    profile_res = client.post("/api/v1/profiles", json={
        "language": "hi",
        "attributes": {
            "annual_family_income": 250000,
            "project_cost": 300000,
            "caste_category": "SC",
            "business_type": "tailoring",
            "business_stage": "new"
        }
    })
    profile_id = profile_res.json()["data"]["profile_id"]

    check_res = client.post("/api/v1/eligibility/check", json={
        "profile_id": profile_id,
        "scheme_ids": ["NBCFDC-GTL-001"]
    })
    assert check_res.status_code == 200
    res_data = check_res.json()["data"]
    assert len(res_data) == 1
    gtl_res = res_data[0]
    assert gtl_res["scheme_id"] == "NBCFDC-GTL-001"
    assert gtl_res["status"] == "ELIGIBLE"
    assert "NBCFDC-INCOME-001" in gtl_res["matched_rules"]
    assert len(gtl_res["failed_rules"]) == 0


def test_eligibility_boundary_and_rejection(client):
    # Income exceeding threshold: 350000 > 300000
    profile_res = client.post("/api/v1/profiles", json={
        "language": "hi",
        "attributes": {
            "annual_family_income": 350000,
            "project_cost": 300000,
            "caste_category": "SC"
        }
    })
    profile_id = profile_res.json()["data"]["profile_id"]

    check_res = client.post("/api/v1/eligibility/check", json={
        "profile_id": profile_id,
        "scheme_ids": ["NBCFDC-GTL-001"]
    })
    assert check_res.status_code == 200
    gtl_res = check_res.json()["data"][0]
    assert gtl_res["status"] == "NOT_ELIGIBLE"
    assert "NBCFDC-INCOME-001" in gtl_res["failed_rules"]


def test_eligibility_missing_information(client):
    # Missing annual_family_income
    profile_res = client.post("/api/v1/profiles", json={
        "language": "hi",
        "attributes": {
            "project_cost": 300000,
            "caste_category": "SC"
        }
    })
    profile_id = profile_res.json()["data"]["profile_id"]

    check_res = client.post("/api/v1/eligibility/check", json={
        "profile_id": profile_id,
        "scheme_ids": ["NBCFDC-GTL-001"]
    })
    assert check_res.status_code == 200
    gtl_res = check_res.json()["data"][0]
    assert gtl_res["status"] == "INSUFFICIENT_INFORMATION"
    assert "annual_family_income" in gtl_res["missing_information"]
