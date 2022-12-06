import logging
from resources import UsersTable
from src.model.userModel import User
from src.model import db


class UserService:

	def __init__(self):
		self.__user_table = UsersTable.UsersTable()

	@staticmethod
	def add_user(email: str, username: str):
		# Validation checks handled at endpoint
		try:
			user = User(username=username,
				 email=email)
			db.session.add(user)
			db.session.commit()
			logging.info('New user added')
			return 'Success'
		except Exception as e:
			logging.fatal('Cannot add new user to database')
			logging.fatal(e)
			return e
