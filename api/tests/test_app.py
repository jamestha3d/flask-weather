import pytest
from app import app, db, City, WeatherRequestLog
from datetime import datetime
import requests
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_weather(client):
    city = City(city_name='London', latitude=51.5074, longitude=-0.1278)
    db.session.add(city)
    db.session.commit()

    with patch('app.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'current': {
                'weather': [{'description': 'clear sky'}],
                'temp': 20
            }
        }
        response = client.get('/weather/1')
        assert response.status_code == 200
        assert b'London' in response.data

def test_get_history(client):
    city = City(city_name='London', latitude=51.5074, longitude=-0.1278)
    db.session.add(city)
    db.session.commit()
    
    log = WeatherRequestLog(
        timestamp=datetime.utcnow(),
        city_id=city.id,
        status='success'
    )
    db.session.add(log)
    db.session.commit()
    
    with patch('app.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'current': {
                'weather': [{'description': 'clear sky'}],
                'temp': 20
            }
        }
        response = client.get('/history')
        assert response.status_code == 200
        assert b'London' in response.data
