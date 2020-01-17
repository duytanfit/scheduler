from flask import Flask, jsonify, request
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

@app.route('/api/mycalendar/events', methods=['GET'])
def get_events():
    dict = {
        "id": "1",
        "text": "Meeting",
        "start_date": "2019-04-11 14:00",
        "end_date": "2019-04-11 17:00",
        "users": "1,2"
    }
    dict2 = {
        "id": "2",
        "text": "Conference",
        "start_date": "2019-04-15 12:00",
        "end_date": "2019-04-18 19:00",
        "users": "1,2"
    }
    dict3 = {
        "id": "3",
        "text": "Interview",
        "start_date": "2019-04-24 09:00",
        "end_date": "2019-04-24 10:00",
        "users": "1,2"
    }

    type1 = {"value": "1", "label": "Interview"}
    type2 = {"value": "2", "label": "Interview2"}
    type3 = {"value": "3", "label": "Interview3"}
    user1 = {"value": "1", "label": 'George' }
    user3 = {"value": "2", "label": 'George2'}
    user4 = {"value": "3", "label": 'George3'}

    return jsonify({'data': [dict, dict2, dict3], 'collections': {'type': [type1, type2, type3],
                                                                           'users': [user1, user3, user4]}})

@app.route('/api/helps/events', methods=['GET'])
def get_helps():

    user1 = {"value": "1", "label": 'George' }
    user3 = {"value": "2", "label": 'George2'}
    user4 = {"value": "3", "label": 'George3'}

    return jsonify([user1, user3, user4])


@app.route('/api/mycalendar/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    post_data = request.get_json()
    print(post_data.get('text'), flush=True)
    return {
        "action": "updated",
        "tid": event_id
    }
app.register_blueprint(auth_blueprint)
if __name__ == '__main__':
    app.run()