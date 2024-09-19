from src import db
from sqlalchemy import func

class Guess(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	guess_date = db.Column(db.DateTime(timezone=False),
						   server_default=func.now(),
						   nullable=False)
	guess_str = db.Column(db.String(35), nullable=False)

	def __init__(self, guess_str, user_id):
		self.guess_str = guess_str
		self.user_id = user_id
