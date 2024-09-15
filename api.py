from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os

from config import Config
from models import db, City, WeatherRequestLog

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/weather/<int:city_id>', methods=['GET'])
def get_weather(city_id):
    city = City.query.get(city_id)
    if not city:
        return jsonify({"error": "City not found"}), 404

    response = requests.get(Config.WEATHER_API_URL, params={
        'lat': city.latitude,
        'lon': city.longitude,
        'exclude': 'hourly,daily',
        'appid': Config.WEATHER_API_KEY
    })

    status = 'success' if response.status_code == 200 else 'failure'
    log = WeatherRequestLog(
        timestamp=datetime.utcnow(),
        city_id=city_id,
        status=status
    )
    db.session.add(log)
    db.session.commit()

    if status == 'failure':
        return jsonify({"error": "Weather API request failed"}), 500

    data = response.json()
    weather_summary = {
        "description": data['current']['weather'][0]['description'],
        "temperature": data['current']['temp']
    }

    return jsonify({
        "city": city.city_name,
        "weather": weather_summary
    })

@app.route('/history', methods=['GET'])
def get_history():
    logs = WeatherRequestLog.query.order_by(WeatherRequestLog.timestamp.desc()).limit(5).all()
    result = []
    for log in logs:
        city = City.query.get(log.city_id)
        response = {
            "timestamp": log.timestamp,
            "city": city.city_name,
            "weather_summary": {
                "description": "Not available",
                "temperature": "Not available"
            }
        }
        if log.status == 'success':
            weather_response = requests.get(Config.WEATHER_API_URL, params={
                'lat': city.latitude,
                'lon': city.longitude,
                'exclude': 'hourly,daily',
                'appid': Config.WEATHER_API_KEY
            })
            data = weather_response.json()
            response['weather_summary'] = {
                "description": data['current']['weather'][0]['description'],
                "temperature": data['current']['temp']
            }
        result.append(response)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
