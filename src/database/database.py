from sqlalchemy import Column, ForeignKey
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Device(db.Model):

    __tablename__ = 'tb_device'
    ID = Column(db.Integer, primary_key=True)
    ID_user = Column(ForeignKey('tb_user.ID'), nullable=False)
    shop_name = Column(db.String(100), nullable=False)
    area = Column(db.Integer, nullable=False)
    max_people = Column(db.Integer, nullable=False)
    current_occupancy = Column(db.Integer, nullable=True)


class User(db.Model):

    __tablename__ = 'tb_user'
    ID = Column(db.Integer, primary_key=True)
    name = Column(db.String(100), nullable=False)
    username = Column(db.String(255), nullable=False)
    password = Column(db.String(100), nullable=False)


class DevicesOccupancy(db.Model):

    __tablename__ = 'tb_devices_occupancy'
    ID = Column(db.String, primary_key=True, nullable=False)
    ID_device = Column(db.Integer, nullable=False)
    timestamp = Column(db.TIMESTAMP, nullable=False)
    occupancy = Column(db.Integer, nullable=False)
