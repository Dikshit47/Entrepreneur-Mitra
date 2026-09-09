"""Tests for Authentication."""


def test_register_and_login(client):
    # 1. Register
    reg_payload = {
        "email": "entrepreneur.test@example.com",
        "phone": "+919988776655",
        "password": "securepassword123",
        "preferred_language": "hi"
    }
    res = client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    token = data["data"]["access_token"]

    # 2. Login
    login_payload = {
        "email_or_phone": "entrepreneur.test@example.com",
        "password": "securepassword123"
    }
    res_login = client.post("/api/v1/auth/login", json=login_payload)
    assert res_login.status_code == 200
    login_data = res_login.json()
    assert login_data["success"] is True
    assert "access_token" in login_data["data"]

    # 3. Access Protected /me endpoint
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/v1/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["data"]["email"] == "entrepreneur.test@example.com"


def test_login_invalid_password(client):
    login_payload = {
        "email_or_phone": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    res = client.post("/api/v1/auth/login", json=login_payload)
    assert res.status_code == 401
    assert res.json()["success"] is False
    assert res.json()["error"]["code"] == "AUTH_REQUIRED"
