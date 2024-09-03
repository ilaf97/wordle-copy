from src import db
from sqlalchemy import Column, DateTime, Integer, String, func


class Guess(db.Model):
	user_id = Column(Integer, primary_key=True)
	guess_date = Column(DateTime(timezone=False),
						   server_default=func.now(),
						   primary_key=True)
	guess_str = Column(String(36), nullable=False)

	def __init__(self, guess_str, user_id):
		self.guess_str = guess_str
		self.user_id = user_id
