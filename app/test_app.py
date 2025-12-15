from app import app

def test_hello():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == "Hello world"
