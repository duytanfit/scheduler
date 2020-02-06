import hashlib
import jwt
import datetime
from database.db import db
class UsersModel(db.Model):
    __tablename__ = "users"

    # thuộc tính
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255))
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    birthday = db.Column(db.DateTime)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)

    #relationship
    events = db.relationship('EventsModel')


    def __init__(self, user_name, password, last_name ='NULL', first_name='NULL', email='NULL',address='NULL',
                 phone_number='NULL', birthday='NULL'):
        self.user_name = user_name
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.birthday = birthday

    def json(self):
        return {
            "value": self.id,
            "label": self.last_name
        }

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'trithan',
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, 'trithan')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @classmethod
    def get_department(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_username(cls, user_name):
        return cls.query.filter_by(user_name=user_name).first()

    @classmethod
    def get_user_in_department(cls, _dep):
        return cls.query.filter_by(department_id=_dep).all()
