import os

class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "mysupersecretkey"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///restaurants.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

