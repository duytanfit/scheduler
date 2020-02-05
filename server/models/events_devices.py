from database.db import db
class EventsDevicesModel(db.Model):
    __tablename__ = "events_devices"
    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    devices = db.relationship("DevicesModel")