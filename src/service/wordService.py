import random
import logging
from data import word_list
from src.model.wordModel import Word
from src.model import db
from src.utils.validations import Validators
from datetime import datetime


class WordService:

	def __init__(self):
		self.word_list = word_list
		self.word_count = self.__count_input_lines()  # Initial length of word list

	@staticmethod
	def add_word(word: str):
		word_validation_error = Validators.word(word)
		if word_validation_error:
			logging.warning(word_validation_error)
		else:
			try:
				word = Word(word)
				db.session.add(word)
				db.session.commit()
				logging.info('New word added')
			except Exception as e:
				logging.error('Cannot add new word to database')
				logging.error(e)

	def get_word(self, date: str = ''):
		if date == '':
			date = self.__get_current_date_str()
		try:
			return Word.query.filter_by(Word.date.contains(date)).word
		except Exception as e:
			logging.warning('Cannot retrieve word from database')
			logging.warning(e)
			return e

	def select_word(self) -> str:
		# This would not be a robust long-term method – improve for demo of architecture understanding
		random_num = random.randint(1, self.word_count)
		try:
			with open(self.word_list) as f:
				for index, line in enumerate(f, start=1):
					if index == random_num:
						word = f.readline()
						self.__delete_word_from_list(word)
		except Exception as e:
			logging.fatal('Could not open word_list.txt file')
			logging.fatal(e)
			word = ''
		return word

	@staticmethod
	def __get_current_date_str() -> str:
		curr_date = datetime.now()
		return datetime.strftime(curr_date, '%Y-%m-%d')

	def __count_input_lines(self) -> int:
		try:
			with open(self.word_list) as f:
				count = 0
				for line in enumerate(f):
					count += 1
				if count == 0:
					raise FileExistsError('No words in word_list.txt')
		except FileExistsError as e:
			logging.fatal(e)
		except Exception as e:
			logging.fatal('Could not open word_list.txt file')
			logging.fatal(e)
		return count

	def __open_word_list_file(self) -> list[str]:
		try:
			with open(self.word_list, 'r') as f:
				return f.readlines()
		except Exception as e:
			logging.warning('Could not open word_list.txt file')
			logging.warning(e)

	def __delete_word_from_list(self, word_to_delete: str):
		# This seems like a strange way of doing things
		try:
			with open(self.word_list, 'w') as f:
				for line in self.__open_word_list_file():
					if line.strip('\n') != word_to_delete:
						f.write(line)
					else:
						logging.info('Word deleted')
						self.word_count -= 1
		except Exception as e:
			logging.warning('Could not open word_list.txt file')
			logging.warning(e)



