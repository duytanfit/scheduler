from database.db import db
class EventsDevicesModel(db.Model):
    __tablename__ = "events_devices"
    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    devices = db.relationship("DevicesModel")

    # khởi tạo
    def __init__(self, event_id, device_id):
        self.event_id = event_id
        self.device_id = device_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_event_by_id(cls, _id):
        return cls.query.filter_by(event_id=_id).all()

    @classmethod
    def find_event_device_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()