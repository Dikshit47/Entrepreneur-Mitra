"""Tests for Conversational AI Interview turns."""


def test_interview_turn_extraction(client):
    # 1. Turn 1: Utterance with business type, stage, and funding
    turn_payload = {
        "input_type": "text",
        "text": "Mujhe silai ka naya business shuru karna hai aur 3 lakh rupaye chahiye.",
        "language": "hi"
    }
    res = client.post("/api/v1/interviews/conv_test_01/turn", json=turn_payload)
    assert res.status_code == 200
    data = res.json()["data"]

    extracted = data["extracted_attributes"]
    assert extracted["business_type"] == "tailoring"
    assert extracted["business_stage"] == "new"
    assert extracted["project_cost"] == 300000
    assert data["next_required_field"] is not None
    assert "district" in data["next_question"].lower() or "rajya" in data["next_question"].lower() or "state" in data["next_question"].lower()


def test_interview_start(client):
    res = client.post("/api/v1/interview/start", json={"language": "hi"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert "greeting" in data
    assert "Entrepreneur Mitra" in data["greeting"]
