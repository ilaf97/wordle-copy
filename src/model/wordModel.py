from src.model import db
from sqlalchemy import *


class Word(db.Model):
	date = Column(DateTime(timezone=False),
						   server_default=func.now(),
						   primary_key=True)
	word = Column(String(5), nullable=False)

