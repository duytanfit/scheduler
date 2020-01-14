from database.db import db
class EventsModel(db.Model):
    __tablename__ = "events"

    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    #relationship
    events_devices = db.relationship('events_devices', backref='events', lazy=True)
    events_users = db.relationship('events_users', backref='events', lazy=True)





