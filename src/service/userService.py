import logging
from src.model.userModel import User
from src import db
from src.utils.exceptions import DatabaseError


class UserService:

	@staticmethod
	def add_user(email: str, username: str, password: str):
		# Validation checks handled at endpoint
		try:
			user = User(
				username=username,
				email=email,
				password=password
			)
			db.session.add(user)
			db.session.commit()
			logging.info(f'New user {username} added')
		except Exception as e:
			logging.error('Cannot add new user to database')
			logging.error(e)
			raise DatabaseError(e)