import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():

    res = client.get("/")
    assert res.json().get('Hello World') == "Jesus Loves You"
    assert res.status_code == 200

def test_network():

    res = client.get("/v1/acn")
    assert res.status_code == 200


def test_program():

    res = client.get("/v1/programs")
    airdate = res.json()[0] 
    today = datetime.date.today().isoformat()
    
    assert airdate.get('airdate') == today
    assert res.status_code == 200

