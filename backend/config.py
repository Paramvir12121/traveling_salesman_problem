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
    OSM_HEADER = os.getenv('OSM_HEADER')
    ORS_API_TOKEN_NAME=os.getenv('ORS_API_TOKEN_NAME')
    ORS_API_TOKEN=os.getenv('ORS_API_TOKEN')