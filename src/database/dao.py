from database.database import db, Device

def add_device(values):

    owner, shop_name, area, max_people = values
    device = Device(owner=owner, shop_name=shop_name, area=area, max_people=max_people)
    db.session.add(device)
    db.session.commit()

def get_max_people(ID):

    return Device.query.filter_by(ID=ID).first()
