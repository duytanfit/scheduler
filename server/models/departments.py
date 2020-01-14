from database.db import db
class DepartmentsModel(db.Model):
    __tablename__ = "departments"

    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    des = db.Column(db.String(255))
    # relaptionship
    users = db.relationship('users', backref='departments', lazy=True)
    events = db.relationship('events', backref='departments', lazy=True)

    # khởi tạo
    def __init__(self, name, des="NULL"):
        self.name = name
        self.des = des

    # # lưu vào db
    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()
    #
    # # xóa từ db
    # def remove_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #
    # # phương thức lớp tìm user từ db theo username
    # @classmethod
    # def find_department_by_id(cls, _id):
    #     return cls.query.filter_by(id=_id).first()
    #






