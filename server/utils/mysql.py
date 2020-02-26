from sqlalchemy import or_, and_
from database.db import db
from models.db_model import *


class MySql:

    '''EVENTS'''

    @staticmethod
    def get_events_in_department(department_id):
        return db.session.query(Event).filter(Event.department_id == department_id).all()

    @staticmethod
    def get_department_of_user(user_id):
        user = db.session.query(User.department_id).filter(User.id == user_id).first()
        return user.department_id

    @staticmethod
    def get_user_in_department(user_id, department_id):
        return db.session.query(User) \
            .filter(User.department_id == department_id, User.id != user_id).all()

    @staticmethod
    def get_all_device():
        return db.session.query(Device.id, Device.name, Type.prefix) \
            .join(Device, Device.type_id == Type.id).all()

    @staticmethod
    def get_device_id():
        return db.session.query(Device.id).all()
    @staticmethod
    def get_all_type():
        return db.session.query(Type.prefix).all()

    @staticmethod
    def get_all_type2():
        return db.session.query(Type).all()

    @staticmethod
    def get_event_of_user(user_id):
        return db.session.query(Event).filter(Event.user_id == user_id).all()

    @staticmethod
    def get_event_invited_of_user(user_id):
        return db.session.query(Event, EventsUser.member_id) \
            .join(EventsUser, Event.id == EventsUser.event_id) \
            .filter(EventsUser.member_id == user_id).all()

    @staticmethod
    def get_event_invited_of_department(department_id):
        return db.session.query(Event, EventsUser.member_id) \
            .join(EventsUser, Event.id == EventsUser.event_id) \
            .filter(Event.department_id == department_id).all()

    @staticmethod
    def get_events_of_device():
        return db.session.query(Event, EventsDevice) \
                .join(EventsDevice, Event.id == EventsDevice.event_id).all()
    @staticmethod
    def get_user_id_of_event(event_id):
        user = db.session.query(Event.user_id).filter(Event.id == event_id).first()
        if user is None:
            return None
        return user.user_id

    @staticmethod
    def get_event_device_by_id(_id):
        return db.session.query(EventsDevice).filter(EventsDevice.id == _id).first()

    @staticmethod
    def get_event_by_id(_id):
        return db.session.query(Event).filter(Event.id == _id).first()
    @staticmethod
    def get_event_user_by_event_member(event_id, user_id):
        return db.session.query(EventsUser) \
            .filter(and_(EventsUser.event_id == event_id, EventsUser.member_id == user_id)).first()

    @staticmethod
    def get_current_device_of_event(device_id, start_date, end_date):
        return db.session.query(Event) \
            .join(EventsDevice, Event.id == EventsDevice.event_id) \
            .filter(and_(EventsDevice.device_id == device_id,
                         or_(and_(start_date <= Event.start_date, end_date >= Event.end_date),
                             and_(end_date > Event.start_date, end_date < Event.end_date),
                             and_(start_date > Event.start_date, start_date < Event.end_date)))).all()

    @staticmethod
    def get_current_device_of_event_for_update(device_id, event_id, start_date, end_date):
        return db.session.query(Event) \
            .join(EventsDevice, Event.id == EventsDevice.event_id) \
            .filter(and_(EventsDevice.device_id == device_id, EventsDevice.event_id != event_id,
                         or_(and_(start_date <= Event.start_date, end_date >= Event.end_date),
                             and_(end_date > Event.start_date, end_date < Event.end_date),
                             and_(start_date > Event.start_date, start_date < Event.end_date)))).all()

    @staticmethod
    def get_device_type_by_event_id(event_id):
        # get id thiet bi, type thiet bi theo id su kien tu database
        return db.session.query(EventsDevice.event_id, Device.id, Type.prefix) \
            .join(EventsDevice, EventsDevice.device_id == Device.id) \
            .join(Type, Device.type_id == Type.id) \
            .filter(EventsDevice.event_id == event_id).all()

    @staticmethod
    def get_invited_user_from_event(event_id):
        return db.session.query(EventsUser.member_id) \
            .join(Event, EventsUser.event_id == Event.id) \
            .filter(EventsUser.event_id == event_id).all()

    @staticmethod
    def get_devices_by_event_id(event_id):
        return db.session.query(EventsDevice).filter(EventsDevice.event_id == event_id).all()

    @staticmethod
    def get_users_by_event_id(event_id):
        return db.session.query(EventsUser).filter(EventsUser.event_id == event_id).all()

    '''UPDATE'''

    @staticmethod
    def update_event(event_id, start_date, end_date, text):
        db.session.query(Event).filter(Event.id == event_id) \
            .update(dict(start_date=start_date, end_date=end_date,
                    text=text), synchronize_session=False)
    '''DELETE'''


    '''COMMIT, ROLLBACK'''

    @staticmethod
    def save_to_db(model=None):
        if model is None:
            db.session.commit()
        else:
            db.session.add(model)
            db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()

    @staticmethod
    def remove_from_db(model):
        db.session.delete(model)
        db.session.commit()
