from Tables import Table
from datetime import datetime
import logging

class WordsTable(Table):

	def __init__(self):
		super().__init__()
		self.create_words_table_sql = 'SQL/Words/CreateWordsTable.sql'
		self.add_word_sql = 'SQL/Words/AddWord.sql'
		self.get_word_sql = 'SQL/Words/GetWord.sql'

	def create_words_table(self):
		self.__create_table(self.create_words_table_sql)

	def add_word(self, word: str):
		conn = self.open_connection()
		sql_command, file = self.__get_command_in_file(self.add_word_sql)
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		try:
			with conn.cursor as cur:
				sql_command = sql_command.replace(
					'[day_date_value]',
					date
				).replace(
					'[word_value]',
					word
				)
				cur.execute(sql_command)
				conn.commit()
		except Exception as e:
			logging.warning('Failed to add word to database')
			logging.warning(e)
		file.close()
		self.close_connection(conn)
		logging.info('Added new word to table')

	def get_word(self, date: str):
		conn = self.open_connection()
		sql_command, file = self.__get_command_in_file(self.get_word_sql)
		try:
			with conn.cursor as cur:
				sql_command = sql_command.replace(
					'[day_date_value]',
					date
				)
				#TODO: Check if can run SQL query searching only on date
				cur.execute(sql_command)
				word = cur.fetchone()
		except Exception as e:
			logging.warning('Failed to get word from database')
			logging.warning(e)
		file.close()
		self.close_connection(conn)
		return word
