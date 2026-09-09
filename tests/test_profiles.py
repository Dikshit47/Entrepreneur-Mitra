"""Tests for Entrepreneur Profile management."""


def test_create_and_update_profile(client):
    # 1. Create Profile
    payload = {
        "language": "hi",
        "attributes": {
            "business_type": "tailoring",
            "business_stage": "new",
            "project_cost": 300000,
            "annual_family_income": 250000,
            "caste_category": "SC",
            "state": "Uttar Pradesh",
            "district": "Bijnor"
        }
    }
    res = client.post("/api/v1/profiles", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]
    assert "profile_id" in data
    assert data["status"] == "draft"
    assert data["completeness_pct"] == 100
    assert data["attributes"]["business_type"] == "tailoring"

    profile_id = data["profile_id"]

    # 2. Get Profile by ID
    res_get = client.get(f"/api/v1/profiles/{profile_id}")
    assert res_get.status_code == 200
    assert res_get.json()["data"]["attributes"]["district"] == "Bijnor"

    # 3. Update Profile
    update_payload = {
        "attributes": {
            "loan_required": 280000,
            "district": "Meerut"
        }
    }
    res_patch = client.patch(f"/api/v1/profiles/{profile_id}", json=update_payload)
    assert res_patch.status_code == 200
    updated_data = res_patch.json()["data"]
    assert updated_data["attributes"]["district"] == "Meerut"
    assert updated_data["attributes"]["loan_required"] == 280000
