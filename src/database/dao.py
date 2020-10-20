from database.database import db, Device


def add_device(values):

    owner, shop_name, area, max_people = values

    ids = [device_id.ID for device_id in Device.query.all()]
    ids.sort()
    last_id = ids[-1]

    device = Device(ID=last_id+1, owner=owner, shop_name=shop_name, area=area, max_people=max_people)
    db.session.add(device)
    db.session.commit()


def get_devices():
    return Device.query.all()


def retrieve_max_people(ID):

    return Device.query.filter_by(ID=ID).first()
