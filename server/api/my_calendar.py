from flask import Blueprint, render_template, jsonify, request, session
from sqlalchemy import or_, and_
from models.devices import DevicesModel
from models.events import EventsModel
from datetime import datetime
import pytz
from database.db import db
from models.events_devices import EventsDevicesModel
from models.events_users import EventsUsersModel
from models.types import TypesModel
from models.users import UsersModel

my_calendar_blueprint = Blueprint('my_calendar', __name__)

@my_calendar_blueprint.route('/api/mycalendar/events', methods=['GET'])
def get_events():
    #get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    #tim department_id tu user_id
    depatment_id = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()

    '''xu li lightbox'''
    # danh sach noi dung cua lightbox
    data = {}
    # danh sach user thuoc phong ban cung voi user x
    list_user = db.session.query(UsersModel).filter(UsersModel.department_id == depatment_id[0], UsersModel.id != user_id).all()
    # danh sach thiet bi
    list_device = db.session.query(DevicesModel.id, DevicesModel.name, TypesModel.prefix).join(DevicesModel,
                                                                                               DevicesModel.type_id == TypesModel.id).all()
    # danh sach loai thiet bi
    list_type = db.session.query(TypesModel.prefix).all()

    #chuan hoa noi dung cho lightbox de truyen den client
    data['users'] = []
    for e in list_type:
        data[e.prefix] = []
    for a in list_device:
        if a.prefix in data:
            data[a.prefix].append({'value': a.id, 'label': a.name})
    for b in list_user:
        data['users'].append({'value': b.id, 'label': b.last_name})

    '''xu li event cua user'''
    list_event = []
    #danh sach cac su kien cua user
    x_event = db.session.query(EventsModel).filter(EventsModel.user_id == user_id).all()
    #danh sach cac su kien ma user duoc moi tham gia

    y_event = db.session.query(EventsModel, EventsUsersModel.member_id) \
        .join(EventsUsersModel, EventsModel.id == EventsUsersModel.event_id) \
        .filter(EventsUsersModel.member_id == user_id).all()

    #chuan hoa noi dung cho su kien
    for x in x_event:
        data2 = SetupContentEvent(x.id)
        data2['id'] = x.id
        data2['text'] = x.text
        data2['start_date'] = x.start_date.strftime('%Y-%m-%d %H:%M')
        data2['end_date'] = x.end_date.strftime('%Y-%m-%d %H:%M')
        data2['user_id'] = x.user_id
        data2['department_id'] = x.department_id
        list_event.append(data2)
    for x in y_event:
        data2 = SetupContentEvent(x[0].id)
        data2['id'] = x[0].id
        data2['text'] = x[0].text
        data2['start_date'] = x[0].start_date.strftime('%Y-%m-%d %H:%M')
        data2['end_date'] = x[0].end_date.strftime('%Y-%m-%d %H:%M')
        data2['user_id'] = x[0].user_id
        data2['department_id'] = x[0].department_id
        list_event.append(data2)
    print(list_event)
    return jsonify({'data': list_event, 'collections': data})

#truyen dong cho lightbox
@my_calendar_blueprint.route('/api/listtype', methods=['GET'])
def get_list():
    list_type = TypesModel.get_all_type()
    return jsonify([u.json2() for u in list_type])

@my_calendar_blueprint.route('/api/mycalendar/events', methods=['POST'])
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

    #check thiet bi hop le
    list_type = db.session.query(TypesModel.prefix).all()

    for y in list_type:
        if post_data[y[0]] != '':
            for i in list(map(int, post_data[y[0]].split(','))):
               if CheckDeviceInvalid(i, local_start_date, local_end_date) == False:
                   return {
                       "action": "error",
                       "message": "device"
                   }, 400

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
@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()

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

        #check thiet bi hop le
        list_type = db.session.query(TypesModel.prefix).all()
        for y in list_type:
            if post_data[y[0]] != '':
                for i in list(map(int, post_data[y[0]].split(','))):
                    if CheckDeviceInvalid2(i,event_id,local_start_date, local_end_date) == False:
                        return {
                                   "action": "error",
                                   "message": "device"
                               }, 400

        # thay doi thong tin o bang event
        EventsModel.update_event_by_id(event_id, local_start_date, local_end_date, post_data['text'], user_id,
                                           depatment_id[0])

        # thay doi thong tin o bang events_devices va events_users
        ChangeContentEvent(post_data)

        return {
             "action": "updated",
             "tid": event_id
        }
    else:
        return{
             "action": "error"
        }



@my_calendar_blueprint.route('/api/mycalendar/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # get user_id tu headers
    auth_header = request.headers.get('Authorization')
    user_id = UsersModel.decode_auth_token(auth_header.split(" ")[1])
    # tim department_id tu user_id
    depatment_id = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()

    # tim user_id cua event
    user = db.session.query(EventsModel.user_id).filter(EventsModel.id == event_id).first()
    if user == None:
        return {
            "action": "error"
        }
    # neu user_id cua event la user_id hien hanh, thi tien hanh xoa noi dung o bang event_users, events_devices va events
    # (nguoi tao su kien thi xoa het)
    if user.user_id == user_id:
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
    elif user.user_id != user_id:
        user2 = db.session.query(EventsUsersModel.id, EventsUsersModel.member_id)\
            .filter(and_(EventsUsersModel.event_id == event_id, EventsUsersModel.member_id == user_id)).all()
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
        .filter(and_(EventsDevicesModel.device_id == device_id, EventsDevicesModel.event_id != event_id, or_(and_(start_date <= EventsModel.start_date, end_date >= EventsModel.end_date),
                                                 and_(end_date > EventsModel.start_date, end_date < EventsModel.end_date),
                                                 and_(start_date > EventsModel.start_date, start_date < EventsModel. end_date)))).all()
    if len(list_event_device) != 0:
        return False

    else:
       return  True