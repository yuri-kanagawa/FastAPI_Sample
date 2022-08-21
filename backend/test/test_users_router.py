import requests
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    end_point = "/user/create/"
    payload = {"user_name":"gijerpg", "password": "gehrog"}
    response = client.post(end_point,
                            json=payload)
    assert response.status_code == 200