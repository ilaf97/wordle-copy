import logging
from src.model.userModel import User
from src import db
from src.utils.exceptions import DatabaseError
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:

	@staticmethod
	def add_user(email: str, username: str, password: str):
		# Validation checks handled at endpoint
		try:
			user = User(
				username=username,
				email=email,
				password=generate_password_hash(password)
			)
			db.session.add(user)
			db.session.commit()
			logging.info(f'New user {username} added')
		except Exception as e:
			logging.error('Cannot add new user to database')
			logging.error(e)
			raise DatabaseError(e)