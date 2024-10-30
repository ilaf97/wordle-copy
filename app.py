import os

from flask import Flask
from src import db
from src.controller import homeController, wordController

def format_sqlite_conn_strings(conn_string: str) -> str:
    return conn_string.split('=')[1].split(';')[0]

def create_production_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.session.commit()
        db.create_all()
    homeController.home_route(app)
    wordController.word_route(app)
    return app


def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['TEST_DATABASE_URL']
    db.init_app(app)
    with app.app_context():
        db.session.commit()
    return app

# try and get something working with the DB
# word_service = WordService(app)
# @app.route('/word/get-word/', defaults={'date': word_service.get_current_date_str()})
# 	@app.route('/word/get-word/<string:date>', methods=['GET'])
# 	def get_word(date: str) -> Any:
# 		check_date = Validators.date_format(date)
# 		# if check_date:
# 		# 	return app.make_response(check_date)
# 		word = word_service.get_word(date)``
# 		if type(word) == Exception:
# 			return app.make_response(500)
#
# 		return f"<h1>{word}<h1>"

if __name__ == "__main__":
    app = create_production_app()
    app.run(debug=True)