from flask import Blueprint, render_template, jsonify, request
from models.events import EventsModel
index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/api/mycalendar/events', methods=['GET'])
def get_events():
    dict = {
        "id": "1",
        "text": "Meeting",
        "start_date": "2020-02-11 14:00",
        "end_date": "2020-02-11 17:00",
        "users": "1,2"
    }
    dict2 = {
        "id": "2",
        "text": "Meeting",
        "start_date": "2020-02-11 14:00",
        "end_date": "2020-02-11 17:00",
        "users": "1,2"
    }
    dict3 = {
        "id": "3",
        "text": "Interview",
        "start_date": "2020-02-11 09:00",
        "end_date": "2020-02-11 10:00",
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


@index_blueprint.route('/api/mycalendar/events', methods=['POST'])
def insert_event():
    post_data = request.get_json()
    print(post_data.get('start_date'))
    event = EventsModel(post_data.get('start_date'), post_data.get('end_date'), post_data.get('text'))
    event.save_to_db()
    return {
        "action": "inserted",
        "tid": event.id
    }


@index_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    post_data = request.get_json()
    print(post_data.get('text'), flush=True)
    return {
        "action": "updated",
        "tid": event_id
    }

@index_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    return {
        "action": "deleted"
    }

