from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Device(db.Model):

    __tablename__ = 'tb_device'
    ID = Column(db.Integer, primary_key=True, autoincrement=True)
    owner = Column(db.String(100), nullable=False)
    shop_name = Column(db.String(100), nullable=False)
    area = Column(db.Integer, nullable=False)
    max_people = Column(db.Integer, nullable=False)
