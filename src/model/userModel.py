from src import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(80), nullable=False)
	
	def __init__(self, username, email):
		self.username = username
		self.email = email

