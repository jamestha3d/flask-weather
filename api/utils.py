from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields
import requests
from datetime import datetime
from .exceptions import APIException
db = SQLAlchemy()

def safe_commit(db):
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise APIException(f"An error occured {e}")
    
class BaseModel(db.Model):
    __abstract__ = True

    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        db.session.add(self)
        safe_commit(db)
        return self

    def delete(self):
        db.session.delete(self)
        safe_commit(db)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise APIException(f"Object has no field {key}")
        self.save()
        return self

    @classmethod
    def create(cls, **kwargs):
        for key in kwargs.keys():
            if not hasattr(cls, key):
                raise APIException(f"Object has no field {key}")
        obj = cls(**kwargs)
        obj.save()
        return obj

    @classmethod
    def get_object(cls, id):
        obj = cls.query.get(id)
        if not obj:
            raise APIException('Resource Not Found', status_code=404)
        return obj 

    @classmethod
    def query_by(cls, **filters):
        return cls.query.filter_by(**filters).all()


def get_reqparse_type(field_type):
    if field_type == fields.Integer:
        return int
    elif field_type == fields.Float:
        return float
    elif field_type == fields.String:
        return str
    elif field_type == fields.Boolean:
        return bool
    elif field_type == fields.DateTime:
        return str
    elif type(field_type) == fields.Nested:
        return dict
    else:
        raise AttributeError(f"Unsupported field type: {field_type}")
    
class ParserGen:
    """ Generic function to get a request parser."""
    def __init__(self, field_dict, required=None):
        self.field_dict = field_dict
        self.parser = reqparse.RequestParser()
        # required = field_dict.keys() if required == '__all__' else required
        self.required = required if required else []
        self._populate_parser()
        
    def _populate_parser(self):
        for field_name, field_type in self.field_dict.items():
            req_type = get_reqparse_type(field_type)
            required = True if field_name in self.required else False
            self.parser.add_argument(field_name, type=req_type, help=f'{field_name} cannot be blank', required=required)

    def get_parser(self):
        return self.parser
    

# class BaseView(Resource):
#     def __init__(self):
#         self.req_parser = reqparse.RequestParser()
#         self.req_parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
#         if hasattr(self, 'arguments'):
#             for arg_name, arg_props in self.arguments.items():
#                 self.req_parser.add_argument(arg_name, **arg_props)

