from database.db import db
from models.events_devices import EventsDevicesModel
from datetime import datetime
class EventsModel(db.Model):
    __tablename__ = "events"

    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20))
    start_date = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    #relationship
    events_devices = db.relationship('EventsDevicesModel')
    events_users = db.relationship('EventsUsersModel')

    # khởi tạo
    def __init__(self, start_date, end_date, text, user_id="NULL", department_id="NULL"):
        self.start_date = start_date
        self.end_date = end_date
        self.text = text
        self.user_id = user_id
        self.department_id = department_id


    # lưu user vào db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # xóa scheduler từ db
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()




