from flask import Blueprint, jsonify, request
from models.db_model import Event
from utils.helps import Helps
from utils.mysql import MySql

device_calendar_blueprint = Blueprint('device_calendar', __name__)


@device_calendar_blueprint.route('/api/device-calendar/events', methods=['GET'])
def get_events():
    user_id = Helps.get_user_id_from_headers()
    department_id = MySql.get_department_of_user(user_id)

    data_color = Helps.random_color_device()
    data = Helps.config_lightbox(user_id, department_id)
    list_event = Helps.config_event_for_device(data_color)
    return jsonify({'data': list_event, 'collections': data})


@device_calendar_blueprint.route('/api/device-calendar/events', methods=['POST'])
def insert_event():
    user_id = Helps.get_user_id_from_headers()
    department_id = MySql.get_department_of_user(user_id)
    post_data = request.get_json()

    # format thoi gian
    local_start_date = Helps.format_time(post_data.get('start_date'))
    local_end_date = Helps.format_time(post_data.get('end_date'))

    list_type = MySql.get_all_type()

    if Helps.is_check_device_Invalid(post_data, list_type, local_start_date, local_end_date):
        try:
            event = Event(local_start_date, local_end_date, post_data.get('text'), user_id, department_id)
            MySql.save_to_db(event)
        except IndentationError:
            MySql.rollback()
            return {"action": "error"}, 400
        if Helps.insert_data_child(post_data, list_type, event=event):
            return {"action": "inserted", "tid": '{}_{}_{}'.format(event.id, user_id, '?')}
        else:
            return {"action": "error"}, 400
    return {"action": "error"}, 400


@device_calendar_blueprint.route('/api/device-calendar/events/<event_id>', methods=['PUT'])
def put_event(event_id):
    post_data = request.get_json()
    user_id = Helps.get_user_id_from_headers()
    event_own_device = list(map(int, event_id.split('_')))
    user_id_of_event = MySql.get_user_id_of_event(event_own_device[0])

    if user_id_of_event == user_id and event_own_device[1] == user_id:
        local_start_date = Helps.format_time(post_data.get('start_date'))
        local_end_date = Helps.format_time(post_data.get('end_date'))
        list_type = MySql.get_all_type()

        if Helps.is_check_device_Invalid(post_data, list_type, local_start_date, local_end_date, event_own_device[0]):
            try:
                MySql.update_event(event_own_device[0], local_start_date, local_end_date, post_data['text'])
                MySql.save_to_db()
            except IndentationError:
                MySql.rollback()
                return {"action": "error"}, 400
            if Helps.insert_data_child(post_data, list_type, event_id=post_data['id_old']):
                return {"action": "updated", "tid": event_id}
            else:
                return {"action": "error"}, 400
        else:
            return {"action": "error"}, 400
    return {"action": "error"}, 400


@device_calendar_blueprint.route('/api/device-calendar/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    user_id = Helps.get_user_id_from_headers()
    event_own_device = list(map(int, event_id.split('_')))
    user_id_of_event = MySql.get_user_id_of_event(event_own_device[0])

    if user_id_of_event is None:
        return {"action": "deleted"}

    if event_own_device[1] == user_id:
        event_device = MySql.get_event_device_by_id(event_own_device[2])
        MySql.remove_from_db(event_device)
        MySql.save_to_db()
        return {"action": "deleted"}
    return {"action": "error"}, 400
