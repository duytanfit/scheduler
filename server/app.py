from flask import Flask, jsonify, request, session
from database.db import db
from auth.views import auth_blueprint
from api.my_calendar import my_calendar_blueprint
from api.department_calendar import department_calendar_blueprint
from api.device_calendar import device_calendar_blueprint
from api.custom_calendar import custom_calendar_blueprint
from flask_cors import CORS
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:2016Unitec@localhost/schedule?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "Unitec"
CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(my_calendar_blueprint)
app.register_blueprint(department_calendar_blueprint)
app.register_blueprint(device_calendar_blueprint)
app.register_blueprint(custom_calendar_blueprint)
app.register_blueprint(auth_blueprint)
if __name__ == '__main__':
    app.run()
