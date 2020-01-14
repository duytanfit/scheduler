from database.db import db
class UsersModel(db.Model):
    __tablename__ = "users"

    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(255))
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    birthday = db.Column(db.DateTime)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    #relationship
    events = db.relationship('events', backref='users', lazy=True)
    events_users = db.relationship('events_users', backref='users', lazy=True)
    roles_users = db.relationship('roles_users', backref='users', lazy=True)





