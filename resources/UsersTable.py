from Tables import Table
from datetime import datetime
import logging


class UsersTable(Table):

	def __init__(self):
		super().__init__()
		self.create_users_table_sql = 'SQL/Users/CreateUsersTable.sql'
		self.add_user_sql = 'SQL/Users/AddUser.sql'
		self.update_user_sql = 'SQL/Users/UpdateUser.sql'

	def create_users_table(self):
		self.__create_table(self.create_users_table_sql)

	def add_user(self, email: str):
		conn = self.open_connection()
		sql_command, file = self.__get_command_in_file(self.add_user_sql)
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		try:
			with conn.cursor as cur:
				sql_command = sql_command.replace(
					'[email_value]',
					email
				).replace(
					'[join_date_value]',
					date
				)
				cur.execute(sql_command)
				conn.commit()
				logging.info('New user successfully created')
		except Exception as e:
			logging.warning('Failed to add user to database')
			logging.warning(e)
		file.close()
		self.close_connection(conn)

	def update_user(self, email: str, user_id: str):
		conn = self.open_connection()
		sql_command, file = self.__get_command_in_file(self.update_users_table_sql)
		try:
			with conn.cursor as cur:
				sql_command = sql_command.replace(
					'[email_value]',
					email
				).replace(
					'[user_id_value]',
					user_id
				)
				cur.execute(sql_command)
				self.conn.commit()
				logging.info(f'User {user_id} successfully updated')
		except Exception as e:
			logging.warning('Failed to update user in database')
			logging.warning(e)
		file.close()
		self.close_connection()
