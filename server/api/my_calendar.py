from datetime import datetime
import pytz
from flask import Blueprint, jsonify

from database.db import db
from models.db_model import Event, EventsDevice, EventsUser
from models.events import EventsModel
from models.events_devices import EventsDevicesModel
from models.events_users import EventsUsersModel
from models.types import TypesModel
from utils.helps import *
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

# truyen dong cho lightbox
@my_calendar_blueprint.route('/api/listtype', methods=['GET'])
def get_list():
    list_type = TypesModel.get_all_type()
    return jsonify([u.json2() for u in list_type])


@my_calendar_blueprint.route('/api/mycalendar/events', methods=['POST'])
def insert_event():
    post_data = request.get_json()
    user_id = Helps.get_user_id_from_headers()
    department_id = MySql.get_department_of_user(user_id)

    local_start_date = Helps.format_time(post_data.get('start_date'))
    local_end_date = Helps.format_time(post_data.get('end_date'))
    list_type = MySql.get_all_type()

    if Helps.is_check_device_Invalid(post_data, list_type, local_start_date, local_end_date):
        event = Event(local_start_date, local_end_date, post_data.get('text'), user_id, department_id)
        MySql.save_to_db(event)

        # insert thiet bi su dung
        Helps.insert_device(post_data, list_type, event)
        return {
            "action": "inserted",
            "tid": event.id
        }
    return {
        "action": "error",

    }, 400




@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = MySql.get_department_of_user(user_id)

    post_data = request.get_json()
    user = db.session.query(EventsModel.user_id).filter(EventsModel.id == post_data['id']).first()
    # kiem tra xem co phai la nguoi tao su kien hay khong
    if user[0] == user_id:
        # format thoi gian
        start_date = datetime.strptime(post_data.get('start_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        end_date = datetime.strptime(post_data.get('end_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        local_start_date = start_date.replace(tzinfo=pytz.utc).astimezone(tz)
        local_end_date = end_date.replace(tzinfo=pytz.utc).astimezone(tz)

        # check thiet bi hop le
        list_type = db.session.query(TypesModel.prefix).all()
        for y in list_type:
            if post_data[y[0]] != '':
                for i in list(map(int, post_data[y[0]].split(','))):
                    if CheckDeviceInvalid2(i, event_id, local_start_date, local_end_date) == False:
                        return {
                                   "action": "error",
                                   "message": "device"
                               }, 400

        # thay doi thong tin o bang event
        EventsModel.update_event_by_id(event_id, local_start_date, local_end_date, post_data['text'], user_id,
                                       depatment_id)

        # thay doi thong tin o bang events_devices va events_users
        ChangeContentEvent(post_data)

        return {
            "action": "updated",
            "tid": event_id
        }
    else:
        return {
            "action": "error"
        }


@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = MySql.get_department_of_user_model(user_id)

    # tim user_id cua event
    user_id_of_ev = MySql.get_user_id_of_event_model(event_id)
    if user_id_of_ev == None:
        return {
            "action": "error"
        }
    # neu user_id cua event la user_id hien hanh, thi tien hanh xoa noi dung o bang event_users, events_devices va events
    # (nguoi tao su kien thi xoa het)
    if user_id_of_ev == user_id:
        for a in EventsDevicesModel.find_event_by_id(event_id):
            a.remove_from_db()
        for b in EventsUsersModel.find_event_by_id(event_id):
            b.remove_from_db()
        event = EventsModel.find_event_by_id(event_id)
        event.remove_from_db()
        return {
            "action": "deleted"
        }
    # kiem tra bang events_users co member_id la user_id hien hanh thi xoa noi dung bang events_users
    # (nguoi duoc moi vao su kien chi duoc thoat khoi su kien, k duoc xoa su kien)
    elif user_id_of_ev != user_id:
        user2 = MySql.get_event_user_by(event_id, user_id)
        print(user2)
        for x in user2:
            ev = EventsUsersModel.find_by_id(x.id)
            ev.remove_from_db()
        return {
            "action": "deleted"
        }
    # tra ve loi neu ca 2TH deu khong thoa man
    return {
        "action": "error"
    }


def SetupContentEvent(event_id):
    # get id thiet bi, type thiet bi theo id su kien tu database
    list_device = db.session.query(EventsDevicesModel.event_id, DevicesModel.id, TypesModel.prefix) \
        .join(EventsDevicesModel, EventsDevicesModel.device_id == DevicesModel.id) \
        .join(TypesModel, DevicesModel.type_id == TypesModel.id) \
        .filter(EventsDevicesModel.event_id == event_id).all()
    # get id user theo su kien tu database
    list_user = db.session.query(EventsUsersModel.member_id) \
        .join(EventsModel, EventsUsersModel.event_id == EventsModel.id) \
        .filter(EventsUsersModel.event_id == event_id).all()
    # get list type thiet bi tu lightbox
    list_type_lightbox = db.session.query(TypesModel.prefix).all()

    # tao dict co cac key la cac thiet bi su dung va users
    data = {}
    data['users'] = []
    for e in list_type_lightbox:
        data[e.prefix] = []

    # set cac thiet bi su dung va users tham gia su kien vao dict
    for y in list_user:
        data['users'].append(y[0])
    for x in list_device:
        if x[2] in data:
            data[x[2]].append(x[1])

    # chuyen value cua dict tu list sang string de phu hop voi thu vien dhtmlxschedule
    for z in data.keys():
        list_to_str = ','.join([str(elem) for elem in data[z]])
        data[z] = list_to_str
    # tra ve danh sach thiet bi su dung va nguoi tham gia su kien trong 1 event
    return data


def ChangeContentEvent(post_data):
    # xoa thiet bi insert lai :v
    for a in EventsDevicesModel.find_event_by_id(post_data['id']):
        a.remove_from_db()
    for b in EventsUsersModel.find_event_by_id(post_data['id']):
        b.remove_from_db()

    # insert thiet bi su dung
    list_type = db.session.query(TypesModel.prefix).all()
    for x in list_type:
        if post_data[x[0]] != '':
            for i in list(map(int, post_data[x[0]].split(','))):
                device_event = EventsDevicesModel(post_data['id'], i)
                device_event.save_to_db()

    # insert thanh vien tham gia
    if post_data['users'] != '':
        for i in list(map(int, post_data['users'].split(','))):
            user_event = EventsUsersModel(post_data['id'], i)
            user_event.save_to_db()


def CheckDeviceInvalid(device_id, start_date, end_date):
    list_event_device = MySql.get_current_device_of_event_model(device_id, start_date, end_date)
    if len(list_event_device) != 0:
        return False
    else:
        return True


def CheckDeviceInvalid2(device_id, event_id, start_date, end_date):
    list_event_device = MySql.get_current_device_of_event_model(device_id, event_id, start_date, end_date)
    if len(list_event_device) != 0:
        return False
    else:
        return True
