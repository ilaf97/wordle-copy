import os
import psycopg2
import uuid
import time
from datetime import datetime
from typing import Tuple, TextIO


class Table:

	def __init__(self):
		self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
		self.create_users_guesses_table_sql = 'SQL/Guesses/CreateGuessesTable.sql'
		self.create_users_table_sql = 'SQL/Users/CreateUsersTable.sql'
		self.create_words_table_sql = 'SQL/Words/CreateWordsTable.sql'
		self.add_user_sql = 'SQL/Users/AddUser.sql'
		self.add_user_guess_sql = 'SQL/Guesses/AddGuess.sql'
		self.update_user_sql = 'SQL/Users/UpdateUser.sql'
		self.add_word_sql = 'SQL/Words/AddWord.sql'

	@staticmethod
	def __get_command_in_file(filename: str) -> Tuple[str, TextIO]:
		file = open(filename, 'r')
		sql_command = file.read()
		return sql_command, file

	def __create_table(self, sql_script):
		sql_command, file = self.__get_command_in_file(sql_script)
		with self.conn.cursor() as cur:
			cur.execute(sql_command)
			self.conn.commit()
		file.close()


