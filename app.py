import os

import sqlalchemy
from flask import Flask
import logging

from sqlalchemy.engine import url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from src.model import db
from src.model.guessModel import Guess
from src.model.wordModel import Word
from src.model.userModel import User

db.init_app(app)

with app.app_context():
	db.create_all()
	logging.info(f'New database tables created:\n'
				 f'- {Guess.__name__}\n'
				 f'- {Word.__name__}\n'
				 f'- {User.__name__}')
