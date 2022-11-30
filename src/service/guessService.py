import logging
from typing import Union
from resources import GuessesTable
from datetime import datetime
from src.model.guessModel import Guess
from src.model import db


class GuessService:
	"""
	A class to handle user guesses.

	Attributes:
		emojis (dict(str)): a dictionary holding the different emoji options
		word (str): the word to guess
		guess_str (str): a string representing all a user's guesses
		guess_num (int): a counter to track the number of guesses made
		__guess_table(GuessesTable): an instance of the GuessesTable class

	Methods:
		add_guess(user_id): sends all user guesses to GuessesTable class to store
			in DB.
		convert_to_emoji(): converts all user guesses to an emoji representation
	"""

	def __init__(self):
		self.__guess_table = GuessesTable.GuessesTable()
		self.emojis = {
			'correct_place': '🟩',
			'correct_letter': '🟨',
			'incorrect_letter': '⬛'
		}
		self.word = ''
		self.guess_str = ''
		self.guess_num = 0
		self.__query = db.session.query_property()

	def add_guess(self, user_id: str) -> Union[None, Exception]:
		"""
		Adds user's final guesses to database.

		Parameters:
			user_id (str): The id of the user making a guess

		Raises:
			ValueError: if no guess has been made
		"""
		try:
			guess = Guess(user_id=user_id,
						  guess_str=self.guess_str)
			db.session.add(guess)
			db.session.commit()
			logging.info('New guess added')
			return 'Success'
		except Exception as e:
				logging.fatal('Cannot add new guess to database')
				logging.fatal(e)
				return e

	@staticmethod
	def get_guesses(date: datetime.date, user_id: int) -> Union[str, Exception]:
		try:
			return Guess.query.filter_by(Guess.guess_date.contains(date), user_id=user_id).guess_str
		except Exception as e:
			logging.warning('Cannot retrieve guess from database')
			logging.warning(e)
			return e


	def convert_to_emoji(self, letter_scores: str) -> str:
		"""
		Converts a complete user guess to a string of emojis representing the
		accuracy of the guesses.

		Returns:
			emoji_str (str): The emoji representation of the guesses
		"""
		emoji_str = ''
		for letter_score in letter_scores:
			if letter_score == '\n':
				emoji_str = emoji_str + '\n'
			elif letter_score == 2:
				emoji_str = emoji_str + self.emojis['correct_place']
			elif letter_score == 1:
				emoji_str = emoji_str + self.emojis['correct_letter']
			else:
				emoji_str = emoji_str + self.emojis['incorrect_letter']
		return emoji_str

	def check_guess(self, guess):
		"""
		Checks the guess against the known word to assess the correctness.
		"""
		letter_scores = '00000'
		for i in range(len(guess)):
			if guess[i] == self.word[i]:
				letter_scores = letter_scores[:i] + 2 + letter_scores[i + 1:]
			elif guess[i] in self.word:
				letter_scores = letter_scores[:i] + 1 + letter_scores[i + 1:]
		return self.convert_to_emoji(letter_scores)
