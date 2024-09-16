from flask import Flask, jsonify
# from flask_restx import Api
# from .views import city_namespace #order_namespace
from config import config_dict
from .utils import db
from .models import City, WeatherRequestLog
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, MethodNotAllowed
from .views import CityView, CityListView, WeatherRequestView, HistoryView
from flask_restful import Api as Router

from .exceptions import APIException

def create_app(config=config_dict['dev']):
    app=Flask(__name__)
    app.config.from_object(config)

    router = Router(app)

    router.add_resource(CityListView, '/cities')
    router.add_resource(CityView, '/city/<int:city_id>')
    router.add_resource(WeatherRequestView, '/weather/<int:city_id>')
    router.add_resource(HistoryView, '/history')

    db.init_app(app)

    migrate = Migrate(app, db)

    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    # @app.errorhandler(Exception)
    # def handle_exception(error):
    #     response = jsonify({"message": "Something went wrong!"})
    #     return response
    
    def make_shell_context():
        return {
            'db': db,
            'city': City,
            'WeatherReport': WeatherRequestLog
        }

    return app