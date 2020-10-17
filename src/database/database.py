from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Device(db.Model):

    __tablename__ = 'tb_device'
    ID = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    owner = Column(String(100), nullable=False)
    shop_name = Column(String(100), nullable=False)
    area = Column(Integer, nullable=False)
    max_people = Column(Integer, nullable=False)
