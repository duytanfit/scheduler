from flask import Blueprint, jsonify, request
from models.db_model import Event
from utils.helps import Helps
from utils.mysql import MySql
department_calendar_blueprint = Blueprint('department_calendar', __name__)


@department_calendar_blueprint.route('/api/department-calendar/events', methods=['GET'])
def get_events():
    user_id = Helps.get_user_id_from_headers()
    department_id = MySql.get_department_of_user(user_id)

    data_color = Helps.random_color_user(user_id, department_id)
    data = Helps.config_lightbox(user_id, department_id)
    list_event = Helps.config_event_for_department(data_color, department_id)
    return jsonify({'data': list_event, 'collections': data})


@department_calendar_blueprint.route('/api/department-calendar/events', methods=['POST'])
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
            return {"action": "error"}, 400
        if Helps.insert_data_child(post_data, list_type, event=event):
            return {"action": "inserted", "tid": '{}_{}'.format(event.id, user_id)}
        else:
            return {"action": "error"}, 400
    return {"action": "error"}, 400

@department_calendar_blueprint.route('/api/department-calendar/events/<event_id>', methods=['PUT'])
def put_event(event_id):
    post_data = request.get_json()
    user_id = Helps.get_user_id_from_headers()
    event_own_id = list(map(int, event_id.split('_')))
    user_id_of_event = MySql.get_user_id_of_event(event_own_id[0])

    if user_id_of_event == user_id and event_own_id[1] == user_id:
        local_start_date = Helps.format_time(post_data.get('start_date'))
        local_end_date = Helps.format_time(post_data.get('end_date'))
        list_type = MySql.get_all_type()

        if Helps.is_check_device_Invalid(post_data, list_type, local_start_date, local_end_date, event_own_id[0]):
            try:
                MySql.update_event(event_own_id[0], local_start_date, local_end_date, post_data['text'])
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

@department_calendar_blueprint.route('/api/department-calendar/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    user_id = Helps.get_user_id_from_headers()
    event_own_id = list(map(int, event_id.split('_')))
    user_id_of_event = MySql.get_user_id_of_event(event_own_id[0])

    if user_id_of_event is None:
        return {"action": "deleted"}

    if user_id_of_event == user_id and event_own_id[1] == user_id:
        for a in MySql.get_devices_by_event_id(event_own_id[0]):
            MySql.remove_from_db(a)
        for b in MySql.get_users_by_event_id(event_own_id[0]):
            MySql.remove_from_db(b)
        ev = MySql.get_event_by_id(event_own_id[0])
        MySql.remove_from_db(ev)
        MySql.save_to_db()
        return {"action": "deleted"}
    if user_id_of_event != user_id and user_id == event_own_id[1]:
        a = MySql.get_event_user_by_event_member(event_own_id[0], user_id)
        MySql.remove_from_db(a)
        MySql.save_to_db()
        return {"action": "deleted"}
    return {"action": "error"}, 400

