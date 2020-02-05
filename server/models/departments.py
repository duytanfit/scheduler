from database.db import db
class DepartmentsModel(db.Model):
    __tablename__ = "departments"

    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    des = db.Column(db.String(255))
    # relaptionship
    users = db.relationship('UsersModel')
    events = db.relationship('EventsModel')

    # khởi tạo
    def __init__(self, name, des="NULL"):
        self.name = name
        self.des = des







