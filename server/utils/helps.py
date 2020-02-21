import pytz
from flask import request
from models.users import UsersModel
from utils.mysql import MySql, datetime
from models.db_model import User, EventsDevice, EventsUser


class Helps:
    @staticmethod
    def get_user_id_from_headers():
        auth_header = request.headers.get('Authorization')
        user_id = User.decode_auth_token(auth_header.split(" ")[1])
        return user_id

    @staticmethod
    def config_lightbox(user_id, department_id):
        list_user = MySql.get_user_in_department(user_id, department_id)
        list_device = MySql.get_all_device()
        list_type = MySql.get_all_type()
        return add_collection(list_user, list_device, list_type)

    @staticmethod
    def config_event(user_id):
        x_event = MySql.get_event_of_user(user_id)

        y_event = MySql.get_event_invited_of_user(user_id)

        return add_device_to_event(x_event, y_event)

    @staticmethod
    def format_time(str_time):
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        return datetime.strptime(str_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc).astimezone(tz)

    @staticmethod
    def is_check_device_Invalid(post_data, list_type, start_date, end_date):
        for y in list_type:
            if post_data[y[0]] != '':
                for i in list(map(int, post_data[y[0]].split(','))):
                    if len(MySql.get_current_device_of_event(i, start_date, end_date)) != 0:
                        return False
        return True

    @staticmethod
    def insert_device(post_data, list_type, event):

        for x in list_type:
            if post_data[x[0]] != '':
                for i in list(map(int, post_data[x[0]].split(','))):
                    device_event = EventsDevice(event.id, i)
                    MySql.save_to_db(device_event)

        # insert thanh vien tham gia
        if post_data['users'] != '':
            for i in list(map(int, post_data['users'].split(','))):
                user_event = EventsUser(event.id, i)
                MySql.save_to_db(user_event)




def SetupContentEvent(event_id):
    # get id thiet bi, type thiet bi theo id su kien tu database
    list_device = MySql.get_device_type_by_event_id(event_id)
    # get id user theo su kien tu database
    list_user = MySql.get_invited_user_from_event(event_id)
    # get list type thiet bi tu lightbox
    list_type_lightbox = MySql.get_all_type()

    # tao dict co cac key la cac thiet bi su dung va users
    data = {'users': []}
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


def add_collection(list_user, list_device, list_type):
    data = {'users': []}
    for e in list_type:
        data[e.prefix] = []
    for a in list_device:
        if a.prefix in data:
            data[a.prefix].append({'value': a.id, 'label': a.name})
    for b in list_user:
        data['users'].append({'value': b.id, 'label': b.last_name})
    return data


def add_device_to_event(my_event, invited_event):
    list_event = []
    for x in my_event:
        data2 = SetupContentEvent(x.id)
        data2['id'] = x.id
        data2['text'] = x.text
        data2['start_date'] = x.start_date.strftime('%Y-%m-%d %H:%M')
        data2['end_date'] = x.end_date.strftime('%Y-%m-%d %H:%M')
        data2['user_id'] = x.user_id
        data2['department_id'] = x.department_id
        list_event.append(data2)
    for x in invited_event:
        data2 = SetupContentEvent(x[0].id)
        data2['id'] = x[0].id
        data2['text'] = x[0].text
        data2['start_date'] = x[0].start_date.strftime('%Y-%m-%d %H:%M')
        data2['end_date'] = x[0].end_date.strftime('%Y-%m-%d %H:%M')
        data2['user_id'] = x[0].user_id
        data2['department_id'] = x[0].department_id
        list_event.append(data2)
    return list_event
