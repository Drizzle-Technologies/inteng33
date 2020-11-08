from .database import db, Device, User, DevicesOccupancy
from ..helper.helper import calculate_max_people
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


def search_by_username(username):

    return User.query.filter_by(username=username).first()


def validate_password(user, password):

    return check_password_hash(user.password, password)


def add_user(values):

    name, username, password = values

    password_hash = generate_password_hash(password)

    ids = [users.ID for users in User.query.all()]
    ids.sort()
    last_id = ids[-1]

    user = User(ID=last_id+1, name=name, username=username, password=password_hash)
    db.session.add(user)
    db.session.commit()
    
    return True


def get_devices():

    return Device.query, db.session.bind


def add_device(values):

    ID_user, shop_name, area, max_people = values

    ids = [device_id.ID for device_id in Device.query.all()]
    ids.sort()
    last_id = ids[-1]

    device = Device(ID=last_id+1, ID_user=ID_user, shop_name=shop_name, area=area, max_people=max_people)
    db.session.add(device)
    db.session.commit()

    return True


def delete_device(ID):
    device = Device.query.filter_by(ID=ID).first()
    db.session.delete(device)
    db.session.commit()
    return True


def get_ID_devices():

    return Device.query.with_entities(Device.ID).distinct(), db.session.bind


def get_user_devices(ID_user):

    return Device.query.filter_by(ID_user=ID_user)


def retrieve_max_people(ID):

    return Device.query.filter_by(ID=ID).first()


def update_max_people(device, area):
    new_max_people = calculate_max_people(area)
    device.max_people = new_max_people

    return True


def update_area(ID, new_area):
    device = Device.query.filter_by(ID=ID).first()
    device.area = new_area

    has_succeded = update_max_people(device, device.area)

    db.session.commit()

    return True and has_succeded


def insert_occupancy(values):

    ID = secrets.token_hex(nbytes=16)
    ID_device, timestamp, occupancy = values

    devices_occupancy = DevicesOccupancy(ID=ID, ID_device=ID_device, timestamp=timestamp, occupancy=occupancy)

    db.session.add(devices_occupancy)
    db.session.commit()


def retrieve_n_occupancy_observations(ID_device, n):

    return DevicesOccupancy.query.filter_by(ID_device=ID_device).limit(n), db.session.bind


def update_current_occupancy(values):

    ID, current_occupancy = values

    device = Device.query.filter_by(ID=ID).first()
    device.current_occupancy = current_occupancy

    db.session.commit()
