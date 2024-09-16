# from flask_restx import Namespace, Resource, fields
from flask_restful import fields, reqparse
from .models import City, WeatherRequestLog
from http import HTTPStatus
from .utils import ParserGen

city_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float
}
weather_summary = {
    'temp': fields.Integer,
    'feels_like': fields.Integer,
    'temp_min': fields.Integer,
    'temp_max': fields.Integer, 
    'description': fields.String,
    'humidity': fields.Integer,
    'icon': fields.String
}
weather_fields = {
    'id': fields.Integer,
    'status': fields.String,
    'city': fields.String,
    'timestamp': fields.DateTime,
    'summary': fields.Nested(weather_summary)
}

id_field = {
    'id': fields.Integer
}

city_update_fields = city_fields.copy()
city_update_fields.pop('id')

city_parser = ParserGen(city_fields).get_parser()
weather_parser = ParserGen(weather_fields).get_parser()
city_update_parser = ParserGen(city_update_fields, required=['name']).get_parser()