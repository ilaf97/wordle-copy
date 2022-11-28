from resources import WordsTable
import random
from typing import TextIO
from math import inf


class WordService:

	def __init__(self):
		self.__word_table = WordsTable.WordsTable()
		self.word_list = './data/word_list.txt'
		self.word_count = 656  # Intial length of word list

	def add_word(self, word: str):
		self.__word_table.add_word(word)

	def __open_word_list_file(self) -> TextIO:
		with open(self.word_list, 'r') as f:
			return f.readlines()

	def __delete_word_from_list(self, word_to_delete: str):
		with open(self.word_list, 'w') as f:
			for line in self.__del_word_from_file():
				if line.strip('\n') != word_to_delete:
					f.write(line)
				else:
					self.word_count -= 1

	def select_word(self) -> str:
		random_num = random.randint(1, self.word_count)
		with open(self.word_list) as f:
			for index, line in enumerate(f, start=1):
				if index == random_num:
					word = f.readline()
					self.__delete_word_from_list(word)
		return word



