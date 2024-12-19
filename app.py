import argparse
import os

from flask_login import LoginManager
from flask import Flask
from etl.user import create_admin_user
from etl.word import run_words_etl
from src import db
from src.controller.wordController import word
from src.controller.guessController import guess
from src.controller.userController import auth
from src.model.userModel import User

def _setup_login_manager(app: Flask) -> None:
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(word, url_prefix='/word')
    app.register_blueprint(guess, url_prefix='/guess')
    app.register_blueprint(auth, url_prefix='/auth')

def format_sqlite_conn_strings(conn_string: str) -> str:
    return conn_string.split('=')[1].split(';')[0]

def create_production_app(re_init_words: bool, create_admin: bool):
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.session.commit()
        # Remove this after building ETL of data
        db.create_all()
        if re_init_words:
            run_words_etl()
        if create_admin:
            create_admin_user()
    
    _setup_login_manager(app)
    return app


def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['TEST_DATABASE_URL']
    db.init_app(app)
    _setup_login_manager(app)
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Wordle Copy Server',
        description='Launch the server for the World Copy game')
    parser.add_argument('-w', '--words', action='store_true', help='Re-initalise words table')
    parser.add_argument('-ad', '--admin', action='store_true', help='Add admin user')
    args = parser.parse_args()
    app = create_production_app(args.words, args.admin)
    app.run(debug=True)