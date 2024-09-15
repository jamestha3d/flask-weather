from api.utils import db

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email=db.Column(db.String(50), nullable=False, unique=True)
    password_hash=db.Column(db.Text(), nullable=False)
    is_staff=db.Column(db.Boolean(), default=False)
    is_active=db.Column(db.Boolean(), default=False)
    orders=db.relationship('Order', backref='customer', lazy=True) #reverse

    def __repr__(self):
        return f"<User {self.username}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(80), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False),
    longitude = db.Column(db.FLoat, nullable=False)

class WeatherRequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    city = db.relationship('City', backref='logs')