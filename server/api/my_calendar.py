from flask import Blueprint, jsonify, request
from models.db_model import Event, EventsDevice, EventsUser
from utils.helps import Helps
from utils.mysql import MySql

my_calendar_blueprint = Blueprint('my_calendar', __name__)


@my_calendar_blueprint.route('/api/mycalendar/events', methods=['GET'])
def get_events():
    user_id = Helps.get_user_id_from_headers()
    department_id = MySql.get_department_of_user(user_id)
    '''xu li light box'''
    data = Helps.config_lightbox(user_id, department_id)
    '''xu li event cua user'''
    list_event = Helps.config_event(user_id)
    return jsonify({'data': list_event, 'collections': data})


@my_calendar_blueprint.route('/api/mycalendar/events', methods=['POST'])
def insert_event():
    post_data = request.get_json()
    user_id = Helps.get_user_id_from_headers()
    department_id = MySql.get_department_of_user(user_id)

    local_start_date = Helps.format_time(post_data.get('start_date'))
    local_end_date = Helps.format_time(post_data.get('end_date'))
    list_type = MySql.get_all_type()

    if Helps.is_check_device_Invalid(post_data, list_type, local_start_date, local_end_date):
        try:
            event = Event(local_start_date, local_end_date, post_data.get('text'), user_id, department_id)
            MySql.save_to_db(event)
        except IndentationError:
            MySql.rollback()
            return {"action": "error", "message": "ERROR: Insert database error"}
        if Helps.insert_data_child(post_data, list_type, event=event):
            return {"action": "success", "tid": event.id, "message": "Inserted"}
        else:
            return {"action": "error", "message": "ERROR: Insert database error"}
    return {"action": "error", "message": "ERROR: The device has been used"}

@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    post_data = request.get_json()
    user_id = Helps.get_user_id_from_headers()
    user_id_of_event = MySql.get_user_id_of_event(event_id)

    if user_id_of_event == user_id:
        local_start_date = Helps.format_time(post_data.get('start_date'))
        local_end_date = Helps.format_time(post_data.get('end_date'))
        list_type = MySql.get_all_type()

        if Helps.is_check_device_Invalid(post_data, list_type, local_start_date, local_end_date, event_id):
            try:
                MySql.update_event(event_id, local_start_date, local_end_date, post_data['text'])
                MySql.save_to_db()
            except IndentationError:
                MySql.rollback()
                return {"action": "error", "message": "ERROR: Insert database error"}
            if Helps.insert_data_child(post_data, list_type, event_id=event_id):
                return {"action": "success", "tid": event_id, "message": "UPDATED"}
            else:
                return {"action": "error", "message": "ERROR: Insert database error"}
        else:
            return {"action": "error", "message": "ERROR: The device has been used"}

    return {"action": "error", "message": "ERROR: Insert database error"}

@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    user_id = Helps.get_user_id_from_headers()
    user_id_of_ev = MySql.get_user_id_of_event(event_id)
    if user_id_of_ev is None:
        return {"action": "success", "message": "DELETED"}

    if user_id_of_ev == user_id:
        for a in MySql.get_devices_by_event_id(event_id):
            MySql.remove_from_db(a)
        for b in MySql.get_users_by_event_id(event_id):
            MySql.remove_from_db(b)
        ev = MySql.get_event_by_id(event_id)
        MySql.remove_from_db(ev)
        MySql.save_to_db()
        return {"action": "success", "message": "DELETED"}
    else:
        a = MySql.get_event_user_by_event_member(event_id, user_id)
        MySql.remove_from_db(a)
        MySql.save_to_db()
        return {"action": "success", "message": "DELETED"}


@my_calendar_blueprint.route('/api/list-type', methods=['GET'])
def get_list():
    list_type = MySql.get_all_type2()
    return jsonify([u.list_type_json() for u in list_type])