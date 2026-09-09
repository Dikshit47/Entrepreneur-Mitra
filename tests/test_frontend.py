"""Frontend Static Integration Tests."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_serve_frontend_root():
    """Verify that root endpoint serves the index.html frontend application."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Entrepreneur Mitra" in response.text
    assert "MoSJE" in response.text


def test_serve_static_assets():
    """Verify that static css and js assets are served properly."""
    css_res = client.get("/static/styles.css")
    assert css_res.status_code == 200
    assert "text/css" in css_res.headers.get("content-type", "")
    assert "--color-navy-primary" in css_res.text

    js_res = client.get("/static/app.js")
    assert js_res.status_code == 200
    assert "javascript" in js_res.headers.get("content-type", "")
    assert "Entrepreneur Mitra" in js_res.text
