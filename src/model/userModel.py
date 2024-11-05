from flask_login import UserMixin
from src import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	email = db.Column(db.String(80), nullable=False, unique=True)
	#TODO: add hashing
	password = db.Column(db.String(30), nullable=False)
	
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password

