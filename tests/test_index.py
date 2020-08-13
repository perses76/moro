from app.main import app

def test_success():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
