import unittest
from api import create_app
from config import config_dict
from api.utils import db
from api.models import WeatherRequestLog
from setup import load_cities
from unittest.mock import patch

mock_data = {
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01n"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 10.53,
        "feels_like": 9.96,
        "temp_min": 9.47,
        "temp_max": 12.16,
        "pressure": 1015,
        "humidity": 89,
        "sea_level": 1015,
        "grnd_level": 994
    },
}
class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client=self.app.test_client()
        db.create_all()
        load_cities()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        self.app=None
        self.client=None

    def test_weather_endpoint(self):

        with patch('api.views.WeatherRequestView') as mock_get:
            id = 5
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_data
            response = self.client.get(f'weather/{id}')
            data = response.get_json()

            assert response.status_code == 200
            log = WeatherRequestLog.query.first()
            assert log is not None
            assert log.city.id == id

    def test_history_endpoint(self):
        with patch('api.views.WeatherRequestView') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_data
            for id in range(1, 7):
                self.client.get(f'weather/{id}')
            response = self.client.get('history')
            data = response.get_json()
            assert len(data) == 5
            