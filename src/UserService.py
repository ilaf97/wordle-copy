from resources import UsersTable


class UserService:

	def __init__(self):
		self.__user_table = UsersTable.UsersTable()

	def add_user(self, email):
		self.__user_table.add_user(email)

	def update_user_email(self, email, user_id):
		self.__user_table.update_user(email, user_id)




