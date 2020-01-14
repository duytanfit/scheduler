from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models.devices import DevicesModel
from models.types import TypesModel
from models.departments import DepartmentsModel
from models.roles import RolesModel
from models.users import UsersModel
from models.roles_users import RolesUsersModel
from models.events import EventsModel
from models.events_devices import EventsDevicesModel
from models.events_users import EventsUsersModel