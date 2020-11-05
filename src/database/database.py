from sqlalchemy import Column, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Device(db.Model):

    __tablename__ = 'tb_device'
    ID = Column(db.Integer, primary_key=True)
    ID_user = Column(ForeignKey('tb_user.ID'), nullable=False)
    shop_name = Column(db.String(100), nullable=False)
    area = Column(db.Integer, nullable=False)
    max_people = Column(db.Integer, nullable=False)


class User(db.Model):

    __tablename__ = 'tb_user'
    ID = Column(db.Integer, primary_key=True)
    name = Column(db.String(100), nullable=False)
    username = Column(db.String(255), nullable=False)
    password = Column(db.String(100), nullable=False)
