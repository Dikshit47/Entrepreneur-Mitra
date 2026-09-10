"""Tests for dynamic interview entity extraction and turn routing."""
import pytest


def test_dynamic_name_and_business_extraction(client):
    payload = {
        "user_message": "Mera naam Priya Sharma hai aur mujhe boutique tailoring ka business shuru karna hai",
        "language": "hi"
    }
    res = client.post("/api/v1/interviews/turn", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    extracted = data["extracted_attributes"]
    assert "name" in extracted
    assert extracted["name"] == "Priya Sharma"
    assert extracted["business_type"] == "tailoring"

    reply = data["assistant_message"]
    assert "Priya Sharma" in reply or "tailoring" in reply
    assert "I have recorded your enterprise details. Let us review the verified government schemes." not in reply


def test_english_name_and_carpentry_extraction(client):
    payload = {
        "text": "My name is Vikram Singh and I run a carpentry workshop",
        "language": "en"
    }
    res = client.post("/api/v1/interviews/conv_dyn_02/turn", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    extracted = data["extracted_attributes"]
    assert extracted.get("name") == "Vikram Singh"
    assert extracted.get("business_type") == "carpentry"
    assert "Vikram Singh" in data["assistant_message"] or "carpentry" in data["assistant_message"]
