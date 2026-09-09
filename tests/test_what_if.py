"""Tests for the What-If Simulator."""


def test_what_if_simulator_hypothetical_isolation(client):
    # 1. Create Profile with Ineligible income: 350,000
    profile_res = client.post("/api/v1/profiles", json={
        "language": "hi",
        "attributes": {
            "business_type": "tailoring",
            "business_stage": "new",
            "project_cost": 300000,
            "annual_family_income": 350000,
            "caste_category": "SC"
        }
    })
    profile_id = profile_res.json()["data"]["profile_id"]

    # 2. Simulate what happens if income is reduced to 250,000
    sim_res = client.post("/api/v1/eligibility/simulate", json={
        "profile_id": profile_id,
        "scheme_id": "NBCFDC-GTL-001",
        "hypothetical_changes": {
            "annual_family_income": 250000
        }
    })
    assert sim_res.status_code == 200
    sim_data = sim_res.json()["data"]

    assert sim_data["is_hypothetical"] is True
    assert sim_data["original"]["decision"] == "NOT_ELIGIBLE"
    assert sim_data["simulated"]["decision"] == "ELIGIBLE"
    assert "NBCFDC-INCOME-001" in sim_data["changed_rules"]
    assert "hypothetical" in sim_data["warning"].lower()

    # 3. CRITICAL: Verify actual profile in database was NOT mutated
    get_res = client.get(f"/api/v1/profiles/{profile_id}")
    actual_income = get_res.json()["data"]["attributes"]["annual_family_income"]
    assert actual_income == 350000
