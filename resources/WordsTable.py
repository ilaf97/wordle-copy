from Tables import Table
from datetime import datetime


class WordsTable(Table):

	def __init__(self):
		super().__init__()
		self.create_words_table_sql = 'SQL/Words/CreateWordsTable.sql'
		self.add_word_sql = 'SQL/Words/AddWord.sql'

	def create_words_table(self):
		self.__create_table(self.create_words_table_sql)

	def add_word(self, word: str):
		sql_command, file = self.__get_command_in_file(self.add_word_sql)
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with self.conn.cursor as cur:
			sql_command = sql_command.replace(
				'[day_date_value]',
				date
			).replace(
				'[word_value]',
				word
			)
			cur.execute(sql_command)
			self.conn.commit()
		file.close()
