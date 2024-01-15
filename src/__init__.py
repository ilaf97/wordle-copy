import logging

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
logging.info('Database instance initialised')
