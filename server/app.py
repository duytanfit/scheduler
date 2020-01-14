from flask import Flask
from database.db import db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:2016Unitec@localhost/test100"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# @app.route('/')
# def hello():
#     return "Hello World!"
db.init_app(app)
with app.app_context():
    db.create_all()