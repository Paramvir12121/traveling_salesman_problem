import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPEN_MAP_API = os.getenv('OPENSTREETMAPAPI')