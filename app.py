import os

from flask import Flask
from src import db
from src.controller import homeController, wordController
from src.scheduled.selectWord import select_new_word

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy()
# logging.info('Database instance initialised')


db.init_app(app)
with app.app_context():
    db.session.commit()

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
