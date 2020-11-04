from database.database import db, Device, User
from helper.helper import calculate_max_people
from werkzeug.security import check_password_hash


def search_by_username(username):

    return User.query.filter_by(username=username).first()


def validate_password(user, password):

    return check_password_hash(user.password, password)

def add_user(values):

    name, username, password = values
    user = User(name, username, password)
    db.session.add(user)
    db.session.commit()
    
    return True

def add_device(values):

    owner, shop_name, area, max_people = values

    ids = [device_id.ID for device_id in Device.query.all()]
    ids.sort()
    last_id = ids[-1]

    device = Device(ID=last_id+1, owner=owner, shop_name=shop_name, area=area, max_people=max_people)
    db.session.add(device)
    db.session.commit()

    return True


def delete_device(ID):
    device = Device.query.filter_by(ID=ID).first()
    db.session.delete(device)
    db.session.commit()
    return True


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

