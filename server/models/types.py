from database.db import db
class TypesModel(db.Model):
    __tablename__ = "types"

    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    prefix = db.Column(db.String(10))

    # relationship
    # devices = db.relationship('devices', backref='types', lazy=True)
    devices = db.relationship('DevicesModel')
    # khởi tạo
    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix

    def json(self):
        return {
            "value": self.id,
            "label": self.name
        }

    @classmethod
    def get_all_type(cls):
        return cls.query.all()

