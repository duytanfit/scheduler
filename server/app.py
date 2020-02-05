from flask import Flask, jsonify, request
from database.db import db
from auth.views import auth_blueprint
from api.mycalendar import index_blueprint
from flask_cors import CORS
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:2016Unitec@localhost/test104"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(index_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run()
