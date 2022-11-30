import os
import psycopg2
import logging
from typing import Tuple, TextIO
from flask_sqlalchemy import SQLAlchemy


class Table:

	def __init__(self):
		# TODO: move conn to main script/service
		self.create_users_guesses_table_sql = 'SQL/Guesses/CreateGuessesTable.sql'
		self.create_users_table_sql = 'SQL/Users/CreateUsersTable.sql'
		self.create_words_table_sql = 'SQL/Words/CreateWordsTable.sql'
		self.add_user_sql = 'SQL/Users/AddUser.sql'
		self.add_user_guess_sql = 'SQL/Guesses/AddGuess.sql'
		self.update_user_sql = 'SQL/Users/UpdateUser.sql'
		self.add_word_sql = 'SQL/Words/AddWord.sql'


	@staticmethod
	def open_connection():
		try:
			connection = psycopg2.connect(os.environ['DATABASE_URL'])
			logging.info('Database connection opened')
			return connection
		except Exception as e:
			logging.fatal("Database connection failed")
			logging.fatal(e)

	@staticmethod
	def close_connection(connection: None):
		connection.close()
		logging.info('Database connection closed')

	@staticmethod
	def __get_command_in_file(filename: str) -> Tuple[str, TextIO]:
		file = open(filename, 'r')
		sql_command = file.read()
		return sql_command, file

	def __create_table(self, sql_script):
		conn = self.open_connection()
		sql_command, file = self.__get_command_in_file(sql_script)
		with conn.cursor() as cur:
			try:
				cur.execute(sql_command)
				conn.commit()
				logging.info('New table created')
			except Exception as e:
				logging.warning('Could not create table')
				logging.warning(e)
		file.close()
		self.close_connection(conn)


