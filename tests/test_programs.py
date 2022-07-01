from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():

    res = client.get("/")
    assert res.json().get('Hello World') == "Jesus Loves You"
    assert res.status_code == 200