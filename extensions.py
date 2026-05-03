from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

db = SQLAlchemy()
login_manager = LoginManager()