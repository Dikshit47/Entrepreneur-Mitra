"""Tests for Multilingual System (English, Hindi, Hinglish)."""
import pytest


def test_multilingual_interview_turns(client):
    # 1. Hindi turn
    hi_turn = client.post("/api/v1/interviews/conv_lang_01/turn", json={
        "text": "मुझे सिलाई का नया काम शुरू करना है और 3 लाख रुपये चाहिए",
        "language": "hi"
    })
    assert hi_turn.status_code == 200
    hi_data = hi_turn.json()["data"]
    assert any(w in hi_data["assistant_message"] for w in ["मैंने", "जानकारी", "व्यवसाय", "राज्य", "जिले"])

    # 2. English turn
    en_turn = client.post("/api/v1/interviews/conv_lang_02/turn", json={
        "text": "I want to start a new tailoring shop with 300000 loan",
        "language": "en"
    })
    assert en_turn.status_code == 200
    en_data = en_turn.json()["data"]
    assert any(w in en_data["assistant_message"] for w in ["recorded", "state", "district", "Understood"])

    # 3. Hinglish turn
    hg_turn = client.post("/api/v1/interviews/conv_lang_03/turn", json={
        "text": "Mujhe silai ka naya business shuru karna hai aur 3 lakh chahiye",
        "language": "hinglish"
    })
    assert hg_turn.status_code == 200
    hg_data = hg_turn.json()["data"]
    assert any(w in hg_data["assistant_message"] for w in ["Maine", "jaankari", "Samajh", "zila", "rajya"])


def test_multilingual_matching_explanations(client):
    # Create test profile
    prof_res = client.post("/api/v1/profiles", json={
        "language": "hi",
        "attributes": {
            "business_type": "tailoring",
            "project_cost": 300000,
            "annual_family_income": 180000,
            "caste_category": "OBC",
            "state": "Uttar Pradesh",
            "district": "Bijnor"
        }
    })
    profile_id = prof_res.json()["data"]["profile_id"]

    # Test Hindi explanation
    hi_expl = client.get(f"/api/v1/matches/NBCFDC-GTL-001/explanation?profile_id={profile_id}&lang=hi")
    assert hi_expl.status_code == 200
    assert "शर्तें" in hi_expl.json()["data"]["summary"] or "मानदंडों" in hi_expl.json()["data"]["summary"]

    # Test English explanation
    en_expl = client.get(f"/api/v1/matches/NBCFDC-GTL-001/explanation?profile_id={profile_id}&lang=en")
    assert en_expl.status_code == 200
    assert "conditions satisfied" in en_expl.json()["data"]["summary"]

    # Test Hinglish explanation
    hg_expl = client.get(f"/api/v1/matches/NBCFDC-GTL-001/explanation?profile_id={profile_id}&lang=hinglish")
    assert hg_expl.status_code == 200
    assert "shartein" in hg_expl.json()["data"]["summary"]
