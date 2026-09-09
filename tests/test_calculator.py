"""Tests for the Financial Calculator."""


def test_emi_calculator(client):
    payload = {
        "loan_amount": 300000,
        "annual_interest_rate": 5.0,
        "tenure_months": 60,
        "moratorium_months": 6,
        "promoter_contribution_pct": 5.0
    }
    res = client.post("/api/v1/calculator/emi", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    # 5% of 300,000 = 15,000
    assert data["promoter_contribution_amount"] == 15000.0
    assert data["effective_repayment_tenure_months"] == 54
    assert data["monthly_emi"] > 0
    assert data["total_payment"] > 300000
    assert "disclaimer" in data
