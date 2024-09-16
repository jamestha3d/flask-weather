# from flask_restx import Namespace, Resource, fields
from .models import City, WeatherRequestLog
from http import HTTPStatus
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask import request, abort
import json
from .serializers import (
    city_fields, city_parser, 
    city_update_parser, weather_fields)
import requests
from config import WEATHER_ENDPOINT
from .exceptions import APIException
from .enums import Status
class Heartbeat(Resource):
    def get(self):
        return {"message": "hello world"}
    
class CityView(Resource):
    @marshal_with(city_fields)
    def get(self, city_id):
        """ Get city"""
        if not isinstance(city_id, int) or city_id <= 0:
            raise APIException('Invalid city_id. Value must be a positive integer')
        city = City.get_object(id=city_id)
        return city, HTTPStatus.OK

    def delete(self, city_id):
        city = City.get_object(city_id)
        city.delete()
        return '', HTTPStatus.NO_CONTENT
    
    @marshal_with(city_fields)
    def put(self, city_id):
        """ Create a new city"""
        city = City.get_object(city_id)
        args = city_update_parser.parse_args()
        args = {key: value for key, value in args.items() if value}
        city = city.update(**args)
        return city, HTTPStatus.CREATED


class CityListView(Resource):
    @marshal_with(city_fields)
    def get(self):
        cities = City.query.all()
        return cities, HTTPStatus.OK
    
    @marshal_with(city_fields)
    def post(self):
        args = city_parser.parse_args()
        city = City.create(**args)
        return city, HTTPStatus.CREATED
    

class WeatherRequestView(Resource):
    def get(self, city_id):
        city = City.get_object(city_id)
        response = city.get_weather_report()
        data = response.json()
        status = Status.SUCCESS.value if response.ok else Status.FAILURE.value
        WeatherRequestLog.log(json.dumps(data), city, status)
        return data, HTTPStatus.OK
    

class HistoryView(Resource):
    @marshal_with(weather_fields)
    def get(self):
        logs = WeatherRequestLog.query.order_by(WeatherRequestLog.created.desc()).limit(5).all()
        return logs, HTTPStatus.OK