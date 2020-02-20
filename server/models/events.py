from database.db import db
from models.events_devices import EventsDevicesModel
import time
from datetime import datetime
class EventsModel(db.Model):
    __tablename__ = "events"
    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20))
    start_date = db.Column(db.DateTime,  nullable=False)
    end_date = db.Column(db.DateTime,  nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    #relationship
    events_devices = db.relationship('EventsDevicesModel')
    events_users = db.relationship('EventsUsersModel')
    # khởi tạo
    def __init__(self, start_date, end_date, text, user_id, department_id):
        self.start_date = start_date
        self.end_date = end_date
        self.text = text
        self.user_id = user_id
        self.department_id = department_id

    def json(self):
        return {
            "id": self.id,
            "text": self.text,
            "start_date": self.start_date.strftime('%Y-%m-%d %H:%M'),
            "end_date": self.end_date.strftime('%Y-%m-%d %H:%M')
        }
    # lưu user vào db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    # xóa scheduler từ db
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_mycalendar(cls):
        return cls.query.all()

    @classmethod
    def get_events_by_user(cls, _user_id):
        return cls.query.filter_by(user_id=_user_id).all()

    @classmethod
    def delete_event_by_id(cls, _id):
        cls.query.filter_by(event_id=_id).first().delete()
        db.session.commit()

    @classmethod
    def find_event_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def update_event_by_id(cls, _id, _start_date, _end_date, _text, _user_id, _department_id):
        cls.query.filter_by(id=_id).update({cls.text: _text, cls.start_date: _start_date, cls.end_date: _end_date,
                                            cls.user_id: _user_id, cls.department_id: _department_id})
        db.session.commit()