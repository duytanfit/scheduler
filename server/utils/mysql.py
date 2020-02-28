from sqlalchemy import or_, and_
from database.db import db_session
from models.db_model import *


class MySql:
    """EVENTS"""

    @staticmethod
    def get_events_in_department(department_id):
        return db_session.query(Event, User.first_name)\
            .join(User, Event.user_id == User.id)\
            .filter(Event.department_id == department_id).all()

    @staticmethod
    def get_user_by_user_name(user_name):
        return db_session.query(User).filter(User.user_name == user_name).first()

    @staticmethod
    def get_department_of_user(user_id):
        user = db_session.query(User.department_id).filter(User.id == user_id).first()
        return user.department_id

    @staticmethod
    def get_user_in_department(user_id, department_id):
        return db_session.query(User) \
            .filter(User.department_id == department_id, User.id != user_id).all()

    @staticmethod
    def get_all_user():
        return db_session.query(User).all()

    @staticmethod
    def get_all_device():
        return db_session.query(Device.id, Device.name, Type.prefix) \
            .join(Device, Device.type_id == Type.id).all()

    @staticmethod
    def get_device_id():
        return db_session.query(Device.id).all()

    @staticmethod
    def get_all_type():
        return db_session.query(Type.prefix).all()

    @staticmethod
    def get_all_type2():
        return db_session.query(Type).all()

    @staticmethod
    def get_event_of_user(user_id):
        return db_session.query(Event).filter(Event.user_id == user_id).all()

    @staticmethod
    def get_event_invited_of_user(user_id):
        return db_session.query(Event, EventsUser.member_id) \
            .join(EventsUser, Event.id == EventsUser.event_id) \
            .filter(EventsUser.member_id == user_id).all()

    @staticmethod
    def get_event_invited_of_department(department_id):
        return db_session.query(Event, EventsUser.member_id, User.first_name) \
            .join(EventsUser, Event.id == EventsUser.event_id) \
            .join(User, EventsUser.member_id == User.id) \
            .filter(Event.department_id == department_id).all()

    @staticmethod
    def get_events_of_device():
        return db_session.query(Event, EventsDevice, Device.name) \
            .join(EventsDevice, Event.id == EventsDevice.event_id)\
            .join(Device, EventsDevice.device_id == Device.id)\
            .all()

    @staticmethod
    def get_user_id_of_event(event_id):
        user = db_session.query(Event.user_id).filter(Event.id == event_id).first()
        if user is None:
            return None
        return user.user_id

    @staticmethod
    def get_event_device_by_id(_id):
        return db_session.query(EventsDevice).filter(EventsDevice.id == _id).first()

    @staticmethod
    def get_event_by_id(_id):
        return db_session.query(Event).filter(Event.id == _id).first()

    @staticmethod
    def get_event_user_by_event_member(event_id, user_id):
        return db_session.query(EventsUser) \
            .filter(and_(EventsUser.event_id == event_id, EventsUser.member_id == user_id)).first()

    @staticmethod
    def get_current_device_of_event(device_id, start_date, end_date):
        return db_session.query(Event) \
            .join(EventsDevice, Event.id == EventsDevice.event_id) \
            .filter(and_(EventsDevice.device_id == device_id,
                         or_(and_(start_date <= Event.start_date, end_date >= Event.end_date),
                             and_(end_date > Event.start_date, end_date < Event.end_date),
                             and_(start_date > Event.start_date, start_date < Event.end_date)))).all()

    @staticmethod
    def get_current_device_of_event_for_update(device_id, event_id, start_date, end_date):
        return db_session.query(Event) \
            .join(EventsDevice, Event.id == EventsDevice.event_id) \
            .filter(and_(EventsDevice.device_id == device_id, EventsDevice.event_id != event_id,
                         or_(and_(start_date <= Event.start_date, end_date >= Event.end_date),
                             and_(end_date > Event.start_date, end_date < Event.end_date),
                             and_(start_date > Event.start_date, start_date < Event.end_date)))).all()

    @staticmethod
    def get_device_type_by_event_id(event_id):
        # get id thiet bi, type thiet bi theo id su kien tu database
        return db_session.query(EventsDevice.event_id, Device.id, Type.prefix) \
            .join(EventsDevice, EventsDevice.device_id == Device.id) \
            .join(Type, Device.type_id == Type.id) \
            .filter(EventsDevice.event_id == event_id).all()

    @staticmethod
    def get_users_in_list(list_user):
        return db_session.query(User.id).filter(User.id.in_(list_user)).all()

    @staticmethod
    def get_invited_user_from_event(event_id):
        return db_session.query(EventsUser.member_id) \
            .join(Event, EventsUser.event_id == Event.id) \
            .filter(EventsUser.event_id == event_id).all()

    @staticmethod
    def get_events_in_list(list_user):
        return db_session.query(Event).filter(Event.user_id.in_(list_user)).all()

    @staticmethod
    def get_event_invited_in_list(list_user):
        return db_session.query(Event, EventsUser.member_id) \
            .join(EventsUser, Event.id == EventsUser.event_id) \
            .filter(EventsUser.member_id.in_(list_user)).all()

    @staticmethod
    def get_devices_by_event_id(event_id):
        return db_session.query(EventsDevice).filter(EventsDevice.event_id == event_id).all()

    @staticmethod
    def get_users_by_event_id(event_id):
        return db_session.query(EventsUser).filter(EventsUser.event_id == event_id).all()

    '''UPDATE'''

    @staticmethod
    def update_event(event_id, start_date, end_date, text):
        db_session.query(Event).filter(Event.id == event_id) \
            .update(dict(start_date=start_date, end_date=end_date,
                         text=text), synchronize_session=False)

    '''DELETE'''

    '''COMMIT, ROLLBACK'''

    @staticmethod
    def save_to_db(model=None):
        if model is None:
            db_session.commit()
        else:
            db_session.add(model)
            db_session.commit()

    @staticmethod
    def rollback():
        db_session.rollback()

    @staticmethod
    def remove_from_db(model):
        db_session.delete(model)
        db_session.commit()
