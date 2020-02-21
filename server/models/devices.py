from database.db import db
from models.types import TypesModel


class DevicesModel(db.Model):
    __tablename__ = "devices"
    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20))
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)

    # khởi tạo
    def __init__(self, name, code):
        self.name = name
        self.code = code

    @classmethod
    def get_devices_by_prefix(cls):
        return cls.query.join(TypesModel, cls.type_id == TypesModel.id).all()
