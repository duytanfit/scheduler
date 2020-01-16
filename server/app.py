from flask import Flask
from database.dbtest import db
from auth.views import auth_blueprint
from flask_cors import CORS
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:2016Unitec@localhost/test101"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

CORS(app)
# @app.route('/')
# def hello():
#     return "Hello World!"
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth_blueprint)
if __name__ == '__main__':
    app.run()