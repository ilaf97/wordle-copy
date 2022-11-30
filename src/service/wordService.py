import random
from src.model.wordModel import Word
from src.model import db
from src.utils.validations import Validators
import logging


class WordService:

	def __init__(self):
		self.word_list = './data/word_list.txt'
		self.word_count = 656  # Initial length of word list

	@staticmethod
	def add_word(word: str):
		word_check = Validators.word(word)
		if word_check:
			logging.warning(word_check)
		else:
			try:
				word = Word(word)
				db.session.add(word)
				db.session.commit()
				logging.info('New word added')
			except Exception as e:
				logging.fatal('Cannot add new word to database')
				logging.fatal(e)

	@staticmethod
	def get_word(date):
		try:
			return Word.query.filter_by(Word.date.contains(date)).word
		except Exception as e:
			logging.warning('Cannot retrieve word from database')
			logging.warning(e)
			return e

	def select_word(self) -> str:
		random_num = random.randint(1, self.word_count)
		with open(self.word_list) as f:
			for index, line in enumerate(f, start=1):
				if index == random_num:
					word = f.readline()
					self.__delete_word_from_list(word)
		return word

	def __open_word_list_file(self) -> list[str]:
		try:
			with open(self.word_list, 'r') as f:
				return f.readlines()
		except Exception as e:
			logging.warning('Could not open word_list file')
			logging.warning(e)

	def __delete_word_from_list(self, word_to_delete: str):
		try:
			with open(self.word_list, 'w') as f:
				for line in self.__open_word_list_file():
					if line.strip('\n') != word_to_delete:
						f.write(line)
					else:
						logging.info('Word deleted')
						self.word_count -= 1
		except Exception as e:
			logging.warning('Could not open word_list file')
			logging.warning(e)



