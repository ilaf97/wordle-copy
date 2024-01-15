from src.model import db


def create_db_app(app):
    db_app = db.init_app(app)
    return db_app
