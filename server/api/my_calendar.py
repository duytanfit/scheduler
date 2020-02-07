from flask import Blueprint, render_template, jsonify, request, session

from models.devices import DevicesModel
from models.events import EventsModel
from datetime import datetime
import time
import json
import pytz
from database.db import db

from models.types import TypesModel
from models.users import UsersModel

my_calendar_blueprint = Blueprint('my_calendar', __name__)

@my_calendar_blueprint.route('/api/mycalendar/events', methods=['GET'])
def get_events():
    all_event = EventsModel.get_all_mycalendar()
    list_user = UsersModel.get_user_in_department(3)
    temp = db.session.query(DevicesModel.id, DevicesModel.name, TypesModel.prefix).join(DevicesModel,
                                                                        DevicesModel.type_id == TypesModel.id).all()
    temp2 = list(db.session.query(TypesModel.prefix).all())

    data = {}
    for e in temp2:
        data[e.prefix] = []

    for a in temp:
        if a.prefix in data:
            data[a.prefix].append({'value': a.id, 'label': a.name})
    print(json.dumps(data))

    return jsonify({'data': [e.json() for e in all_event], 'collections': data})

@my_calendar_blueprint.route('/api/listtest', methods=['GET'])
def get_listtest():
    dict = {
        "value": 1,
        "label": "Interview"
    }
    dict2 = {
        "value": 1,
        "label": "Interview"
    }
    return jsonify([dict, dict2])

@my_calendar_blueprint.route('/api/listtype', methods=['GET'])
def get_list():
    list_type = TypesModel.get_all_type()
    return jsonify([u.json2() for u in list_type])

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

