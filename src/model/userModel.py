from sqlalchemy import Column, DateTime, Integer, String, func
from src import db


class User(db.Model):
	id = Column(Integer, primary_key=True)
	username = Column(String(20), nullable=False)
	email = Column(String(80), nullable=False)
	join_date = Column(DateTime(timezone=False),
						   server_default=func.now())
	
	def __init__(self, username, email):
		self.username = username
		self.email = email

