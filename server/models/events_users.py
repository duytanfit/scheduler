from database.db import db
class EventsUsersModel(db.Model):
    __tablename__ = "events_users"
    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
