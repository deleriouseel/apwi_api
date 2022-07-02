import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():

    res = client.get("/")
    assert res.json().get('Hello World') == "Jesus Loves You"
    assert res.status_code == 200


def test_network_acn():

    res = client.get("/v1/acn")
    network = res.json()[0]

    assert len(res.json()) == 20
    assert network.get('network') == 'ACN'
    assert res.status_code == 200


def test_network_search():

    res = client.get("/v1/acn?search=peter")
    search = res.json()[0].get('title')
   
    assert "Peter" in search
    assert res.status_code == 200


def test_network_date():
    res = client.get("/v1/calvary/2022-03-03")
    date = res.json()[0].get('airdate')
  
    assert "2022-03-03" in date
    assert res.status_code == 200


def test_network_daterange():
    res = client.get("/v1/calvary/2022-04-01?end_date=2022-04-05")
    dates = len(res.json())

    assert dates == 3
    assert res.status_code == 200


def test_program():

    res = client.get("/v1/programs")
    airdate = res.json()[0]
    today = datetime.date.today().isoformat()
    
    assert len(res.json()) == 40
    assert airdate.get('airdate') == today
    assert res.status_code == 200


def test_program_search():

    res = client.get("/v1/programs?search=colossians")
    search = res.json()[0].get('title')
   
    assert "Colossians" in search
    assert res.status_code == 200
