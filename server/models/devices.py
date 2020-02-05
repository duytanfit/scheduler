from database.db import db
class DevicesModel(db.Model):
    __tablename__ = "devices"
    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20))
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)

    #relationship
    # events_devices = db.relationship('events_devices', back_populates='devices', lazy=True)

    # khởi tạo
    def __init__(self, name, code):
        self.name = name
        self.code = code

    # def __repr__(self):
    #     return '<Devicename %r>' % self.name



