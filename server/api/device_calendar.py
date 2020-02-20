import numpy as np
from flask import Blueprint, render_template, jsonify, request, session
from sqlalchemy import or_, and_
from models.devices import DevicesModel
from models.events import EventsModel
from datetime import datetime
import time
import json
import pytz
from database.db import db
from models.events_devices import EventsDevicesModel
from models.events_users import EventsUsersModel

from models.types import TypesModel
from models.users import UsersModel

device_calendar_blueprint = Blueprint('device_calendar', __name__)

@device_calendar_blueprint.route('/api/device-calendar/events', methods=['GET'])
def get_events():
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()

    # ramdom mau cho moi device
    data_color = {}
    color_list_device = db.session.query(DevicesModel.id).all()
    for x in color_list_device:
        data_color['{}'.format(x.id)] = "#{:06x}".format(np.random.randint(0, 0xFFFFFF))

    # chuan hoa noi dung cho lightbox de truyen den client
    list_user = db.session.query(UsersModel).filter(UsersModel.department_id == depatment_id[0], UsersModel.id != user_id).all()
    list_device = db.session.query(DevicesModel.id, DevicesModel.name, TypesModel.prefix)\
        .join(DevicesModel, DevicesModel.type_id == TypesModel.id).all()
    list_type = db.session.query(TypesModel.prefix).all()

    data = {}
    data['users'] = []
    for e in list_type:
        data[e.prefix] = []
    for a in list_device:
        if a.prefix in data:
            data[a.prefix].append({'value': a.id, 'label': a.name})
    for b in list_user:
        data['users'].append({'value': b.id, 'label': b.last_name})

    '''chuan hoa noi dung cho su kien'''
    list_event = []
    # nhung su kien co su dung thiet bi
    event_device = db.session.query(EventsModel, EventsDevicesModel)\
        .join(EventsDevicesModel, EventsModel.id == EventsDevicesModel.event_id).all()
    for x in event_device:
        x_data = SetupContentEvent(x[0].id)
        x_data['id_old'] = x[0].id
        x_data['text'] = x[0].text
        x_data['start_date'] = x[0].start_date.strftime('%Y-%m-%d %H:%M')
        x_data['end_date'] = x[0].end_date.strftime('%Y-%m-%d %H:%M')
        x_data['user_id'] = x[0].user_id
        x_data['department_id'] = x[0].department_id
        x_data['id'] = '{}_{}_{}'.format(x[0].id, x[0].user_id, x[1].id)
        x_data['textColor'] = "#000000"
        if str(x[1].device_id) in data_color:
            x_data['color'] = data_color[str(x[1].device_id)]
        list_event.append(x_data)
    return jsonify({'data': list_event, 'collections': data})

#truyen dong cho lightbox
@device_calendar_blueprint.route('/api/listtype', methods=['GET'])
def get_list_type():
    list_type = TypesModel.get_all_type()
    return jsonify([u.json2() for u in list_type])

@device_calendar_blueprint.route('/api/device-calendar/events', methods=['POST'])
def insert_event():
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()

    post_data = request.get_json()
    #format thoi gian
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
                if CheckDeviceInvalid(i, local_start_date, local_end_date) == False:
                    return {
                               "action": "error",
                               "message": "device"
                           }, 400

    #tam thay session bang bien cu the

    # print(session['id'])
    user = UsersModel.get_department(user_id)
    event = EventsModel(local_start_date, local_end_date, post_data.get('text'), user_id, user.department_id)
    event.save_to_db()

    #insert thiet bi su dung
    for x in list_type:
        if post_data[x[0]] != '':
            for i in list(map(int, post_data[x[0]].split(','))):
                device_event = EventsDevicesModel(event.id, i)
                device_event.save_to_db()

    #insert thanh vien tham gia
    if post_data['users'] != '':
        for i in list(map(int, post_data['users'].split(','))):
            user_event = EventsUsersModel(event.id, i)
            user_event.save_to_db()

    return {
        "action": "inserted",
        "tid": event.id
    }
@device_calendar_blueprint.route('/api/device-calendar/events/<event_id>', methods=['PUT'])
def put_event(event_id):
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()


    event_user_device_id = list(map(int, event_id.split('_')))
    post_data = request.get_json()

    # kiem tra xem co phai la nguoi tao su kien hay khong
    if event_user_device_id[1] == user_id:
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
                    if CheckDeviceInvalid2(i,event_user_device_id[0],local_start_date, local_end_date) == False:
                        return {
                                   "action": "error",
                                   "message": "device"
                               }, 400

        # thay doi thong tin o bang event
        EventsModel.update_event_by_id(post_data['id_old'], local_start_date, local_end_date, post_data['text'], user_id,
                                           post_data['department_id'])

        # thay doi thong tin o bang events_devices va events_users
        ChangeContentEvent(post_data)

        return {
             "action": "updated",
             "tid": event_id
        }
    else:
        return{
             "action": "error"
        }, 400


@device_calendar_blueprint.route('/api/device-calendar/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()
    event_user_device_id = list(map(int, event_id.split('_')))

    if len(event_user_device_id) <= 1:
        return {
                   "action": "error"
               }, 400

    if event_user_device_id[1] == user_id:
        event_device = EventsDevicesModel.find_event_device_by_id(event_user_device_id[2])
        print(event_device)
        event_device.remove_from_db()
        return {
            "action": "deleted"
        }
    return {
        "action": "error"
    }, 400

def SetupContentEvent(event_id):
    #get id thiet bi, type thiet bi theo id su kien tu database
    list_device = db.session.query(EventsDevicesModel.event_id, DevicesModel.id, TypesModel.prefix)\
        .join(EventsDevicesModel, EventsDevicesModel.device_id == DevicesModel.id)\
        .join(TypesModel, DevicesModel.type_id == TypesModel.id)\
        .filter(EventsDevicesModel.event_id == event_id).all()
    #get id user theo su kien tu database
    list_user = db.session.query(EventsUsersModel.member_id)\
        .join(EventsModel, EventsUsersModel.event_id == EventsModel.id)\
        .filter(EventsUsersModel.event_id == event_id).all()
    #get list type thiet bi tu lightbox
    list_type_lightbox = db.session.query(TypesModel.prefix).all()

    #tao dict co cac key la cac thiet bi su dung va users
    data = {}
    data['users'] = []
    for e in list_type_lightbox:
        data[e.prefix] = []

    #set cac thiet bi su dung va users tham gia su kien vao dict
    for y in list_user:
        data['users'].append(y[0])
    for x in list_device:
        if x[2] in data:
            data[x[2]].append(x[1])

    #chuyen value cua dict tu list sang string de phu hop voi thu vien dhtmlxschedule
    for z in data.keys():
        list_to_str = ','.join([str(elem) for elem in data[z]])
        data[z] = list_to_str
    #tra ve danh sach thiet bi su dung va nguoi tham gia su kien trong 1 event
    return data

def ChangeContentEvent(post_data):
    #xoa thiet bi insert lai :v
    for a in EventsDevicesModel.find_event_by_id(post_data['id_old']):
        a.remove_from_db()
    for b in EventsUsersModel.find_event_by_id(post_data['id_old']):
        b.remove_from_db()

    # insert thiet bi su dung
    list_type = db.session.query(TypesModel.prefix).all()
    for x in list_type:
        if post_data[x[0]] != '':
            for i in list(map(int, post_data[x[0]].split(','))):
                device_event = EventsDevicesModel(post_data['id_old'], i)
                device_event.save_to_db()

    # insert thanh vien tham gia
    if post_data['users'] != '':
        for i in list(map(int, post_data['users'].split(','))):
            user_event = EventsUsersModel(post_data['id_old'], i)
            user_event.save_to_db()

def CheckDeviceInvalid(device_id,start_date,end_date):
    list_event_device = db.session.query(EventsModel)\
        .join(EventsDevicesModel, EventsModel.id == EventsDevicesModel.event_id)\
        .filter(and_(EventsDevicesModel.device_id == device_id, or_(and_(start_date <= EventsModel.start_date, end_date >= EventsModel.end_date),
                                                 and_(end_date > EventsModel.start_date, end_date < EventsModel.end_date),
                                                 and_(start_date > EventsModel.start_date, start_date < EventsModel.end_date)))).all()
    if len(list_event_device) != 0:
        return False

    else:
       return  True

def CheckDeviceInvalid2(device_id,event_id,start_date,end_date):
    list_event_device = db.session.query(EventsModel)\
        .join(EventsDevicesModel, EventsModel.id == EventsDevicesModel.event_id)\
        .filter(and_(EventsDevicesModel.device_id == device_id,EventsDevicesModel.event_id != event_id, or_(and_(start_date <= EventsModel.start_date, end_date >= EventsModel.end_date),
                                                 and_(end_date > EventsModel.start_date, end_date < EventsModel.end_date),
                                                 and_(start_date > EventsModel.start_date, start_date < EventsModel. end_date)))).all()
    if len(list_event_device) != 0:
        return False

    else:
       return  True