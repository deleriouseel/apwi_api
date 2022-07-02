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

    assert network.get('network')  == 'ACN'
    assert res.status_code == 200

def test_network_calvary():

    res = client.get("/v1/calvary")
    network = res.json()[0]

    assert network.get('network')  == 'CALVARY'
    assert res.status_code == 200 

def test_network_search():

    res = client.get("/v1/acn?search=peter")
    search = res.json()[0].get('title')
    
    assert "Peter" in search
    assert res.status_code == 200

def test_network_date():
    res = client.get("/v1/acn/2022-03-03")
    date = res.json()[0].get('airdate')
   
    assert "2022-03-03" in date
    assert res.status_code == 200


def test_program():

    res = client.get("/v1/programs")
    airdate = res.json()[0] 
    today = datetime.date.today().isoformat()
    
    assert airdate.get('airdate') == today
    assert res.status_code == 200

def test_program_search():

    res = client.get("/v1/programs?search=colossians")
    search = res.json()[0].get('title')
    
    assert "Colossians" in search
    assert res.status_code == 200       

