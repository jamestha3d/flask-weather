import unittest
from api import create_app
from api.config.config import config_dict
from api.utils import db
from werkzeug.security import generate_password_hash
from api.models.orders import Order
from flask_jwt_extended import create_access_token
class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client=self.app.test_client()
        
        db.create_all()
    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        self.app=None
        self.client=None

    def test_get_all_orders(self):
        token = create_access_token(identity='testuser')
        headers = {
            "Authorization": f'Bearer {token}'
        }
        data = {
            "username": "testuser",
            "email": "testuser@company.com",
            "password": "password" 
        }
        response = self.client.get(
            'orders/orders', headers=headers
        )

        assert response.status_code == 200
        assert response.json == []
        

