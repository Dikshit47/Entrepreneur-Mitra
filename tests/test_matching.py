"""Tests for Scheme Matching and Ranking."""


def test_matching_pipeline_and_ranking(client):
    profile_res = client.post("/api/v1/profiles", json={
        "language": "hi",
        "attributes": {
            "business_type": "tailoring",
            "business_stage": "new",
            "project_cost": 300000,
            "annual_family_income": 200000,
            "caste_category": "SC",
            "state": "Uttar Pradesh",
            "district": "Bijnor"
        }
    })
    profile_id = profile_res.json()["data"]["profile_id"]

    match_res = client.post("/api/v1/matches", json={"profile_id": profile_id})
    assert match_res.status_code == 200
    data = match_res.json()["data"]
    assert "results" in data
    assert len(data["results"]) > 0

    top_match = data["results"][0]
    assert top_match["scheme_id"] == "NBCFDC-GTL-001"
    assert top_match["status"] == "ELIGIBLE"
    assert top_match["match_score"] >= 80

    # Verify score breakdown presence
    breakdown = top_match["score_breakdown"]
    assert "eligibility_completeness" in breakdown
    assert "purpose_fit" in breakdown
    assert "financial_fit" in breakdown

    # Verify explanation endpoint
    expl_res = client.get(f"/api/v1/matches/{top_match['scheme_id']}/explanation?profile_id={profile_id}")
    assert expl_res.status_code == 200
    expl_data = expl_res.json()["data"]
    assert expl_data["decision"] == "ELIGIBLE"
    assert len(expl_data["criteria"]) > 0
    assert expl_data["official_url"] != ""
