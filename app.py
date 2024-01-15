import logging
import os
from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src import db
from src.controller import homeController, wordController
from src.service.wordService import WordService
from src.scheduled.selectWord import select_new_word
from src.utils.validations import Validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from src.model.guessModel import Guess
from src.model.wordModel import Word
from src.model.userModel import User

# db = SQLAlchemy()
# logging.info('Database instance initialised')


db.init_app(app)
with app.app_context():
    db.session.commit()
    db.create_all()
    logging.info(f'New database tables created:\n'
                 f'- {Guess.__name__}\n'
                 f'- {Word.__name__}\n'
                 f'- {User.__name__}')

select_new_word(app)

homeController.home_route(app)
wordController.word_route(app)

# try and get something working with the DB
# word_service = WordService(app)
# @app.route('/word/get-word/', defaults={'date': word_service.get_current_date_str()})
# 	@app.route('/word/get-word/<string:date>', methods=['GET'])
# 	def get_word(date: str) -> Any:
# 		check_date = Validators.date_format(date)
# 		# if check_date:
# 		# 	return app.make_response(check_date)
# 		word = word_service.get_word(date)
# 		if type(word) == Exception:
# 			return app.make_response(500)
#
# 		return f"<h1>{word}<h1>"


if __name__ == "__main__":
    app.run(debug=True)
