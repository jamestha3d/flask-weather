import unittest
from api import create_app
from api.config.config import config_dict
from api.utils import db
from werkzeug.security import generate_password_hash
from api.models.users import User

class UserTestCase(unittest.TestCase):
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

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "testuser@company.com",
            "password": "password" 
        }
        response = self.client.post(
            'auth/signup', json=data
        )
        

        user = User.query.filter_by(email=data['email']).first()
        assert user.username == data['username']
        assert response.status_code == 201

    def test_login(self):
        data = {
            "email": "testuser@company.com",
            "password": "password" 
        }
        response = self.client.post(
            'auth/login', json=data
        )

        assert response.status_code == 400