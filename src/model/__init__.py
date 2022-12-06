from flask_sqlalchemy import SQLAlchemy
import logging


db = SQLAlchemy()
logging.info('Database instance initialised')
