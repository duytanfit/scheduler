from flask import Blueprint, render_template, jsonify, request, session
from models.events import EventsModel
from datetime import datetime
import time
import json
import pytz

from models.types import TypesModel
from models.users import UsersModel

my_calendar_blueprint = Blueprint('my_calendar', __name__)

@my_calendar_blueprint.route('/api/mycalendar/events', methods=['GET'])
def get_events():
    all_event = EventsModel.get_all_mycalendar()
    list_user = UsersModel.get_user_in_department(3)
    list_type = TypesModel.get_all_type()
    return jsonify({'data': [e.json() for e in all_event], 'collections': {'users': [u.json() for u in list_user],
        'devices': [d.json() for d in list_type]}})

@my_calendar_blueprint.route('/api/mycalendar/events', methods=['POST'])
def insert_event():
    post_data = request.get_json()
    print(post_data)
    start_date = datetime.strptime(post_data.get('start_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
    end_date = datetime.strptime(post_data.get('end_date'), '%Y-%m-%dT%H:%M:%S.%fZ')

    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    local_start_date = start_date.replace(tzinfo=pytz.utc).astimezone(tz)
    local_end_date = end_date.replace(tzinfo=pytz.utc).astimezone(tz)

    #tam thay session bang bien cu the
    my_id = 1
    # print(session['id'])
    user = UsersModel.get_department(my_id)
    event = EventsModel(local_start_date, local_end_date, post_data.get('text'), my_id, user.department_id)
    event.save_to_db()
    return {
        "action": "inserted",
        "tid": event.id
    }

@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    post_data = request.get_json()
    print(post_data.get('text'), flush=True)
    return {
        "action": "updated",
        "tid": event_id
    }

@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    return {
        "action": "deleted"
    }

