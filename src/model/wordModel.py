from sqlalchemy import *
from src import db


class Word(db.Model):
    __tablename__ = "word"
    date = Column(DateTime(timezone=False),
                  server_default=func.now(),
                  primary_key=True)
    word = Column(String(5), nullable=False)
