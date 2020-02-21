from sqlalchemy import or_, and_
from database.db import db
from models.db_model import *


class MySql:
    @staticmethod
    def get_department_of_user(user_id):
        user = db.session.query(User.department_id).filter(User.id == user_id).first()
        return user.department_id

    # @staticmethod
    # def get_department_of_user_model(user_id):
    #     user = db.session.query(UsersModel.department_id).filter(UsersModel.id == user_id).first()
    #     return user.department_id

    @staticmethod
    def get_user_in_department(user_id, department_id):
        return db.session.query(User) \
            .filter(User.department_id == department_id, User.id != user_id).all()

    # @staticmethod
    # def get_user_in_department_model(user_id, department_id):
    #     return db.session.query(UsersModel) \
    #         .filter(UsersModel.department_id == department_id, UsersModel.id != user_id).all()

    @staticmethod
    def get_all_device():
        return db.session.query(Device.id, Device.name, Type.prefix) \
            .join(Device, Device.type_id == Type.id).all()

    # @staticmethod
    # def get_all_device_model():
    #     return db.session.query(DevicesModel.id, DevicesModel.name, TypesModel.prefix) \
    #         .join(DevicesModel, DevicesModel.type_id == TypesModel.id).all()

    @staticmethod
    def get_all_type():
        return db.session.query(Type.prefix).all()

    # @staticmethod
    # def get_all_type_model():
    #     return db.session.query(TypesModel.prefix).all()

    @staticmethod
    def get_event_of_user(user_id):
        return db.session.query(Event).filter(Event.user_id == user_id).all()

    # @staticmethod
    # def get_event_of_user_model(user_id):
    #     return db.session.query(EventsModel).filter(EventsModel.user_id == user_id).all()

    @staticmethod
    def get_event_invited_of_user(user_id):
        return db.session.query(Event, EventsUser.member_id) \
            .join(EventsUser, Event.id == EventsUser.event_id) \
            .filter(EventsUser.member_id == user_id).all()

    # @staticmethod
    # def get_event_invited_of_user_model(user_id):
    #     return db.session.query(EventsModel, EventsUsersModel.member_id) \
    #         .join(EventsUsersModel, EventsModel.id == EventsUsersModel.event_id) \
    #         .filter(EventsUsersModel.member_id == user_id).all()

    @staticmethod
    def get_user_id_of_event(event_id):
        user = db.session.query(Event.user_id).filter(Event.id == event_id).first()
        if user == None:
            return None
        return user.user_id

    # @staticmethod
    # def get_user_id_of_event_model(event_id):
    #     user = db.session.query(EventsModel.user_id).filter(EventsModel.id == event_id).first()
    #     if user == None:
    #         return None
    #     return user.user_id

    @staticmethod
    # chua toi uu
    def get_event_user_by(event_id, user_id):
        return db.session.query(EventsUser.id, EventsUser.member_id) \
            .filter(and_(EventsUser.event_id == event_id, EventsUser.member_id == user_id)).all()

    # @staticmethod
    # # chua toi uu
    # def get_event_user_by(event_id, user_id):
    #     return db.session.query(EventsUsersModel.id, EventsUsersModel.member_id) \
    #         .filter(and_(EventsUsersModel.event_id == event_id, EventsUsersModel.member_id == user_id)).all()

    @staticmethod
    def get_current_device_of_event(device_id, start_date, end_date):
        return db.session.query(Event) \
            .join(EventsDevice, Event.id == EventsDevice.event_id) \
            .filter(and_(EventsDevice.device_id == device_id,
                         or_(and_(start_date <= Event.start_date, end_date >= Event.end_date),
                             and_(end_date > Event.start_date, end_date < Event.end_date),
                             and_(start_date > Event.start_date, start_date < Event.end_date)))).all()

    # @staticmethod
    # def get_current_device_of_event_model(device_id, start_date, end_date):
    #     return db.session.query(EventsModel) \
    #         .join(EventsDevicesModel, EventsModel.id == EventsDevicesModel.event_id) \
    #         .filter(and_(EventsDevicesModel.device_id == device_id,
    #                      or_(and_(start_date <= EventsModel.start_date, end_date >= EventsModel.end_date),
    #                          and_(end_date > EventsModel.start_date, end_date < EventsModel.end_date),
    #                          and_(start_date > EventsModel.start_date, start_date < EventsModel.end_date)))).all()

    @staticmethod
    def get_current_device_of_event2(device_id, event_id, start_date, end_date):
        return db.session.query(Event) \
            .join(EventsDevice, Event.id == Event.event_id) \
            .filter(and_(EventsDevice.device_id == device_id, EventsDevice.event_id != event_id,
                         or_(and_(start_date <= Event.start_date, end_date >= Event.end_date),
                             and_(end_date > Event.start_date, end_date < Event.end_date),
                             and_(start_date > Event.start_date, start_date < Event.end_date)))).all()

    # @staticmethod
    # def get_current_device_of_event_model(device_id, event_id, start_date, end_date):
    #     return db.session.query(EventsModel) \
    #         .join(EventsDevicesModel, EventsModel.id == EventsDevicesModel.event_id) \
    #         .filter(and_(EventsDevicesModel.device_id == device_id, EventsDevicesModel.event_id != event_id,
    #                      or_(and_(start_date <= EventsModel.start_date, end_date >= EventsModel.end_date),
    #                          and_(end_date > EventsModel.start_date, end_date < EventsModel.end_date),
    #                          and_(start_date > EventsModel.start_date, start_date < EventsModel.end_date)))).all()

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
    def save_to_db(model):
        db.session.add(model)
        db.session.commit()


