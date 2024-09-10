from sqlalchemy import func
from src import db


class Word(db.Model):
    __tablename__ = "word"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False)
    selected_date = db.Column(db.DateTime(timezone=False),
                  server_default=func.now())

    def __init__(self, word: str):
        self.word = word
