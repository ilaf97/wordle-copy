from resources.Tables import Table
from datetime import datetime
import logging


class GuessesTable(Table):

	def __init__(self):
		super().__init__()
		self.create_guesses_table_sql = 'SQL/Guesses/CreateGuessesTable.sql'
		self.add_user_guess_sql = 'SQL/Guesses/AddGuess.sql'

	def create_guesses_table(self):
		self.__create_table(self.create_users_guesses_table_sql)

	def add_user_guess(self, user_id: str, guess_list: list):
		conn = self.open_connection()
		sql_command, file = self.__get_command_in_file(self.add_user_guess_sql)
		date = datetime.now()
		date_of_guess = date.strftime('%Y-%m-%d %H:%M:%S')
		datestamp = date.strftime('%d%m%Y')
		guess_id = user_id + '_' + datestamp
		try:
			with conn.cursor() as cur:
				sql_command = sql_command.replace(
					'[guess_id_value]',
					guess_id
				).replace(
					'[user_id_value]',
					user_id
				).replace(
					'[date_of_guess_value]',
					date_of_guess
				).replace(
					'[guess_arr_value]',
					guess_list
				)
				cur.execute(sql_command)
				conn.commit()
		except Exception as e:
			logging.warning('Failed to add guess to database')
			logging.warning(e)
		file.close()
		logging.info('User guess added')
		self.close_connection(conn)

# TODO: get user guess from DB
