from src import db


class Word(db.Model):
    __tablename__ = "word"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False, unique=True)
    selected_date = db.Column(db.DateTime(timezone=False))

    def __init__(self, word: str):
        self.word = word
