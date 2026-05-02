from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    mail = Column(String(128), unique=True, nullable=False)
    fullname = Column(String(128), nullable=False)
    password = Column(String(256), nullable=False)
    role = Column(String(20), default="user")
