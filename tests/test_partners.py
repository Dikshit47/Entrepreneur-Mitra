"""Tests for Geo-spatial Partner Locator."""


def test_nearby_partners_locator(client):
    # Ramesh location in Bijnor: lat=29.3724, lng=78.1358
    res = client.get("/api/v1/partners/nearby?lat=29.3724&lng=78.1358&radius_km=100")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) >= 1

    closest = data[0]
    assert closest["district"] == "Bijnor"
    assert closest["distance_km"] < 5.0
    assert closest["status"] == "VERIFIED"
    assert closest["fund_utilisation_status"] == "AVAILABLE"
