from datetime import datetime
import jwt
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from database.db import Base


class Department(Base):
    __tablename__ = 'departments'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20))
    des = Column(String(255))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20))
    des = Column(String(255))


class Type(Base):
    __tablename__ = 'types'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20))
    prefix = Column(String(10))

    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix

    def json(self):
        return {
            "value": self.id,
            "label": self.name
        }

    def list_type_json(self):
        return {
            "prefix": self.prefix,
            "name": self.name
        }


class Device(Base):
    __tablename__ = 'devices'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50))
    code = Column(String(20))
    type_id = Column(ForeignKey('types.id'), nullable=False, index=True)

    type = relationship('Type')


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    user_name = Column(String(20), primary_key=True)
    password = Column(String(255))
    last_name = Column(String(20))
    first_name = Column(String(20))
    email = Column(String(50))
    address = Column(String(100))
    phone_number = Column(String(20))
    birthday = Column(DateTime)
    department_id = Column(ForeignKey('departments.id'), index=True)

    department = relationship('Department')

    def __init__(self, user_name, password, department, last_name='NULL', first_name='NULL', email='NULL', address='NULL',
                 phone_number='NULL', birthday=None):
        self.user_name = user_name
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.birthday = birthday
        self.department_id = department

    def json(self):
        return {
            "value": self.id,
            "label": self.last_name
        }

    def json2(self):
        return {
            "userID": self.id,
            "username": self.user_name
        }

    def json_list_user(self):
        return {
            "id": self.id,
            "text": self.last_name
        }


class Event(Base):
    __tablename__ = 'events'

    id = Column(INTEGER(11), primary_key=True)
    text = Column(String(20))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    user_id = Column(ForeignKey('users.id'), index=True)
    department_id = Column(ForeignKey('departments.id'), index=True)

    department = relationship('Department')
    user = relationship('User')

    def __init__(self, start_date, end_date, text, user_id, department_id):
        self.start_date = start_date
        self.end_date = end_date
        self.text = text
        self.user_id = user_id
        self.department_id = department_id


class RolesUser(Base):
    __tablename__ = 'roles_users'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    role_id = Column(ForeignKey('roles.id'), nullable=False, index=True)

    role = relationship('Role')
    user = relationship('User')


class EventsDevice(Base):
    __tablename__ = 'events_devices'

    id = Column(INTEGER(11), primary_key=True)
    event_id = Column(ForeignKey('events.id'), nullable=False, index=True)
    device_id = Column(ForeignKey('devices.id'), nullable=False, index=True)

    device = relationship('Device')
    event = relationship('Event')

    def __init__(self, event_id, device_id):
        self.event_id = event_id
        self.device_id = device_id


class EventsUser(Base):
    __tablename__ = 'events_users'

    id = Column(INTEGER(11), primary_key=True)
    event_id = Column(ForeignKey('events.id'), nullable=False, index=True)
    member_id = Column(ForeignKey('users.id'), nullable=False, index=True)

    event = relationship('Event')
    member = relationship('User')

    def __init__(self, event_id, member_id):
        self.event_id = event_id
        self.member_id = member_id
