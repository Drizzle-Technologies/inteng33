from database.database import db, Device, User
from werkzeug.security import check_password_hash


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


def search_by_username(username):

    return User.query.filter_by(username=username).first()


def validate_password(user, password):

    return check_password_hash(user.password, password)

