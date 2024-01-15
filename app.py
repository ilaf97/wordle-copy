import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.controller import homeController, wordController
from src.service import *
from src.scheduled.selectWord import select_new_word

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from src.model.guessModel import Guess
from src.model.wordModel import Word
from src.model.userModel import User

db = SQLAlchemy()
logging.info('Database instance initialised')

select_new_word()

db.init_app(app)
homeController.home_route(app)
wordController.word_route(app, db)

with app.app_context():
    db.create_all()
    logging.info(f'New database tables created:\n'
                 f'- {Guess.__name__}\n'
                 f'- {Word.__name__}\n'
                 f'- {User.__name__}')

if __name__ == "__main__":
    app.run(debug=True)
