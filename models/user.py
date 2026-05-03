from extensions import db, Column, Integer, String
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    mail = Column(String(128), unique=True, nullable=False)
    fullname = Column(String(128), nullable=False)
    password = Column(String(256), nullable=False)
    role = Column(String(20), default="user")
    