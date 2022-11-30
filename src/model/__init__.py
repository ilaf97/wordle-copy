from flask_sqlalchemy import SQLAlchemy
from app import app
import logging

db = SQLAlchemy(app)
logging.info('Database instance initialised')
