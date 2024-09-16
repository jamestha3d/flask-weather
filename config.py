import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

import os
uri = os.getenv('DATABASE_URL')

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

WEATHER_ENDPOINT = f"https://api.openweathermap.org/data/3.0/onecall?lat={{lat}}&lon={{lon}}&appid={API_KEY}"
OPEN_WEATHER_ENDPOINT = f"https://api.openweathermap.org/data/2.5/weather?q={{city}}&appid={API_KEY}&units=metric"

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')

class DevConfig(Config):
    DEBUG = bool(os.getenv('DEBUG'))
    SQLACHEMY_TRACK_MODIFICATIONS=False
    # SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///' +os.path.join(BASE_DIR, 'db.sqlite3') #uri
    
class TestConfig(Config):
    TESTING=True
    DEBUG = True
    SQLACHEMY_TRACK_MODIFICATIONS=False
    # SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite://' #use in memory db

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL')
    SQLACHEMY_TRACK_MODIFICATIONS=False
    DEBUG = bool(os.getenv('DEBUG'))

config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,

}