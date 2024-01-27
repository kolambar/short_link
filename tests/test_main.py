import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_short_link():
    with pytest.raises(AttributeError):  # чтобы не было проблем при логировании
        response = client.post("/short_link/", json={"link": "https://example.com"})
        assert response.status_code == 200
        assert response.json() is not None


def test_create_short_link_with_no_json():
    response = client.post("/short_link/")
    assert response.status_code == 422


