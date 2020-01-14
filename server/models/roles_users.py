from database.db import db
class RolesUsersModel(db.Model):
    __tablename__ = "roles_users"
    # thuộc tính
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)


