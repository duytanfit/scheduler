import numpy as np
import pytz
from flask import request
from utils.mysql import MySql, datetime
from models.db_model import User, EventsDevice, EventsUser
from auth.views import get_current_user

class Helps:
    @staticmethod
    def get_user_id_from_headers():
        auth_header = request.headers.get('Authorization')
        return get_current_user(auth_header.split(" ")[1])['identity']

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
    def config_event_for_department(data_color, department_id):
        x_event = MySql.get_events_in_department(department_id)
        y_event = MySql.get_event_invited_of_department(department_id)
        return add_device_to_event_for_department(data_color, x_event, y_event)

    @staticmethod
    def config_event_for_device(data_color):
        event_device = MySql.get_events_of_device()
        return add_device_to_event_for_device(data_color, event_device)

    @staticmethod
    def config_event_for_search(data_color, list_user):
        x_event = MySql.get_events_in_list(list_user)
        y_event = MySql.get_event_invited_in_list(list_user)
        return add_device_to_event_for_department(data_color, x_event, y_event)

    @staticmethod
    def format_time(str_time):
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        return datetime.strptime(str_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc).astimezone(tz)

    @staticmethod
    def is_check_device_Invalid(post_data, list_type, start_date, end_date, event_id=None):
        if event_id is None:
            for y in list_type:
                if post_data[y[0]] != '':
                    for i in list(map(int, post_data[y[0]].split(','))):
                        if len(MySql.get_current_device_of_event(i, start_date, end_date)) != 0:
                            return False
            return True
        else:
            for y in list_type:
                if post_data[y[0]] != '':
                    for i in list(map(int, post_data[y[0]].split(','))):
                        if len(MySql.get_current_device_of_event_for_update(i, event_id, start_date, end_date)) != 0:
                            return False
            return True

    @staticmethod
    def insert_data_child(post_data, list_type, event_id=None, event=None):
        if event is None:
            for a in MySql.get_devices_by_event_id(event_id):
                try:
                    MySql.remove_from_db(a)
                except IndentationError:
                    return False
            for b in MySql.get_users_by_event_id(event_id):
                try:
                    MySql.remove_from_db(b)
                except IndentationError:
                    return False

            # insert thiet bi su dung
            for x in list_type:
                if post_data[x[0]] != '':
                    for i in list(map(int, post_data[x[0]].split(','))):
                        try:
                            ev = EventsDevice(event_id, i)
                            MySql.save_to_db(ev)
                        except IndentationError:
                            return False

            # insert thanh vien tham gia
            if post_data['users'] != '':
                for i in list(map(int, post_data['users'].split(','))):
                    try:
                        ev = EventsUser(event_id, i)
                        MySql.save_to_db(ev)
                    except IndentationError:
                        return False
            return True
        else:
            for x in list_type:
                if post_data[x[0]] != '':
                    for i in list(map(int, post_data[x[0]].split(','))):
                        try:
                            device_event = EventsDevice(event.id, i)
                            MySql.save_to_db(device_event)
                        except IndentationError:
                            return False

            # insert thanh vien tham gia
            if post_data['users'] != '':
                for i in list(map(int, post_data['users'].split(','))):
                    try:
                        user_event = EventsUser(event.id, i)
                        MySql.save_to_db(user_event)
                    except IndentationError:
                        return False
            return True

    @staticmethod
    def random_color_user(user_id, department_id):
        data_color = {}
        x_list_user = MySql.get_user_in_department(user_id, department_id)
        for x in x_list_user:
            data_color['{}'.format(x.id)] = "#{:06x}".format(np.random.randint(0, 0xFFFFFF))
        return data_color

    @staticmethod
    def random_color_device():
        data_color = {}
        color_list_device = MySql.get_device_id()
        for x in color_list_device:
            data_color['{}'.format(x.id)] = "#{:06x}".format(np.random.randint(0, 0xFFFFFF))
        return data_color

    @staticmethod
    def random_color_search(list_user):
        data_color = {}
        x_list_user = MySql.get_users_in_list(list_user)
        for x in x_list_user:
            data_color['{}'.format(x.id)] = "#{:06x}".format(np.random.randint(0, 0xFFFFFF))
        return data_color

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


def add_device_to_event_for_department(data_color, my_event, invited_event):
    list_event = []
    for x in my_event:
        x_data = SetupContentEvent(x[0].id)
        x_data['id_old'] = x[0].id
        x_data['text'] = x[0].text
        x_data['start_date'] = x[0].start_date.strftime('%Y-%m-%d %H:%M')
        x_data['end_date'] = x[0].end_date.strftime('%Y-%m-%d %H:%M')
        x_data['user_id'] = x[0].user_id
        x_data['department_id'] = x[0].department_id
        x_data['own'] = x[0].user_id
        x_data['first_name'] = x[1]
        x_data['id'] = '{}_{}'.format(x[0].id, x[0].user_id)
        x_data['textColor'] = "#000000"
        if str(x_data['own']) in data_color:
            x_data['color'] = data_color[str(x[0].user_id)]
        list_event.append(x_data)

    for x in invited_event:
        x_data = SetupContentEvent(x[0].id)
        x_data['id_old'] = x[0].id
        x_data['text'] = x[0].text
        x_data['start_date'] = x[0].start_date.strftime('%Y-%m-%d %H:%M')
        x_data['end_date'] = x[0].end_date.strftime('%Y-%m-%d %H:%M')
        x_data['user_id'] = x[0].user_id
        x_data['department_id'] = x[0].department_id
        x_data['own'] = x[1]
        x_data['first_name'] = x[2]
        x_data['id'] = '{}_{}'.format(x[0].id, x[1])
        x_data['textColor'] = "#000000"
        if str(x_data['own']) in data_color:
            x_data['color'] = data_color[str(x[1])]
        list_event.append(x_data)
    return list_event


def add_device_to_event_for_device(data_color, event_device):
    list_event = []
    for x in event_device:
        x_data = SetupContentEvent(x[0].id)
        x_data['id_old'] = x[0].id
        x_data['text'] = x[0].text
        x_data['start_date'] = x[0].start_date.strftime('%Y-%m-%d %H:%M')
        x_data['end_date'] = x[0].end_date.strftime('%Y-%m-%d %H:%M')
        x_data['user_id'] = x[0].user_id
        x_data['department_id'] = x[0].department_id
        x_data['name_device'] = x[2]
        x_data['id'] = '{}_{}_{}'.format(x[0].id, x[0].user_id, x[1].id)
        x_data['textColor'] = "#000000"
        if str(x[1].device_id) in data_color:
            x_data['color'] = data_color[str(x[1].device_id)]
        list_event.append(x_data)
    return list_event


# def add_device_to_event_for_search(data_color, my_event, invited_event):
#     list_event = []
#     for x in my_event:
#         x_data = SetupContentEvent(x.id)
#         x_data['id_old'] = x.id
#         x_data['text'] = x.text
#         x_data['start_date'] = x.start_date.strftime('%Y-%m-%d %H:%M')
#         x_data['end_date'] = x.end_date.strftime('%Y-%m-%d %H:%M')
#         x_data['user_id'] = x.user_id
#         x_data['department_id'] = x.department_id
#         x_data['own'] = x.user_id
#         x_data['id'] = '{}_{}'.format(x.id, x.user_id)
#         x_data['textColor'] = "#000000"
#         if str(x_data['own']) in data_color:
#             x_data['color'] = data_color[str(x.user_id)]
#         list_event.append(x_data)
#
#     for x in invited_event:
#         x_data = SetupContentEvent(x[0].id)
#         x_data['id_old'] = x[0].id
#         x_data['text'] = x[0].text
#         x_data['start_date'] = x[0].start_date.strftime('%Y-%m-%d %H:%M')
#         x_data['end_date'] = x[0].end_date.strftime('%Y-%m-%d %H:%M')
#         x_data['user_id'] = x[0].user_id
#         x_data['department_id'] = x[0].department_id
#         x_data['own'] = x[1]
#         x_data['id'] = '{}_{}'.format(x[0].id, x[1])
#         x_data['textColor'] = "#000000"
#         if str(x_data['own']) in data_color:
#             x_data['color'] = data_color[str(x[1])]
#         list_event.append(x_data)
#     return list_event

