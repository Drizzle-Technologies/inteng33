from .database import db, Device, User, DevicesOccupancy
from ..helper.helper import calculate_max_people
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


class UserDao:

    @staticmethod
    def search_by_username(username):
        """Method seacrches a user by his or her username."""

        return User.query.filter_by(username=username).first()

    @staticmethod
    def validate_password(user, password):
        """Method validates a password by comparing the stored hash to the input password."""

        return check_password_hash(user.password, password)

    @staticmethod
    def add_user(values):
        """Method adds a new user to the User table."""

        name, username, password = values

        password_hash = generate_password_hash(password)

        ids = [users.ID for users in User.query.all()]
        if not ids:
            ids = [0]
        ids.sort()
        last_id = ids[-1]

        user = User(ID=last_id+1, name=name, username=username, password=password_hash)
        db.session.add(user)
        db.session.commit()

        return True


class DeviceDao:

    @staticmethod
    def get_devices():
        """Method gets all the devices stored in the Device table and returns the session bind"""

        return Device.query, db.session.bind

    @staticmethod
    def add_device(values):
        """Method adds a new device to the Device table"""

        ID_user, shop_name, area, max_people = values

        ids = [device_id.ID for device_id in Device.query.all()]
        if not ids:
            ids = [0]
        ids.sort()
        last_id = ids[-1]

        device = Device(ID=last_id+1, ID_user=ID_user, shop_name=shop_name, area=area, max_people=max_people)
        db.session.add(device)
        db.session.commit()

        return True

    @staticmethod
    def delete_device(ID):
        """Method deletes device from the Device table by searching by id"""

        device = Device.query.filter_by(ID=ID).first()
        db.session.delete(device)
        db.session.commit()
        return True

    @staticmethod
    def get_ID_devices():
        """Gets the ids from all the devices"""

        return Device.query.with_entities(Device.ID).distinct(), db.session.bind

    @staticmethod
    def get_user_devices(ID_user):
        """Gets the devices from a specific user thourgh the user's id"""

        return Device.query.filter_by(ID_user=ID_user)

    @staticmethod
    def retrieve_max_people(ID):
        """Retrieves the max number of people allowed in a device's building by searching by ID."""

        return Device.query.filter_by(ID=ID).first()

    @staticmethod
    def update_max_people(device, area):
        """Updates the max number of people allowed in a device's building by passing the device's object"""

        new_max_people = calculate_max_people(area)
        device.max_people = new_max_people

        return True

    def update_area(self, ID, new_area):
        """Updates the area and max_people through the device's ID in the Device table"""

        device = Device.query.filter_by(ID=ID).first()
        device.area = new_area

        has_succeded = self.update_max_people(device, device.area)

        db.session.commit()

        return True and has_succeded


class DeviceOccupancyDao:

    @staticmethod
    def insert_occupancy(values):
        """Inserts a new occupancy record in DevicesOccupancy"""

        ID = secrets.token_hex(nbytes=16)
        ID_device, timestamp, occupancy = values

        devices_occupancy = DevicesOccupancy(ID=ID, ID_device=ID_device, timestamp=timestamp, occupancy=occupancy)

        db.session.add(devices_occupancy)
        db.session.commit()

    @staticmethod
    def retrieve_n_occupancy_observations(ID_device):
        """Retrieves 100 rows of occupancy observations from DevicesOccupancy"""

        return DevicesOccupancy.query.filter_by(ID_device=ID_device).order_by(DevicesOccupancy.timestamp.desc()).limit(100),\
               db.session.bind

    @staticmethod
    def update_current_occupancy(values):
        """Updates the current occupancy in the Devices table"""

        ID, current_occupancy = values

        device = Device.query.filter_by(ID=ID).first()
        device.current_occupancy = current_occupancy

        db.session.commit()
