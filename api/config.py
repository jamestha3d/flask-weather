import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

uri = os.getenv('DATABASE_URL')

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

debug = bool(os.getenv('DEBUG'))
local_db = 'sqlite:///' +os.path.join(BASE_DIR, 'db.sqlite3')


class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30)
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')

class DevConfig(Config):
    DEBUG = debug
    SQLACHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///' +os.path.join(BASE_DIR, 'db.sqlite3') #uri
    
class TestConfig(Config):
    TESTING=True
    DEBUG = True
    SQLACHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
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