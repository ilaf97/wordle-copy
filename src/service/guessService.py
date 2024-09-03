import logging
from typing import Union
from resources import GuessesTable
from datetime import datetime
from src.model.guessModel import Guess
from src.service.wordService import WordService
from app import db


class GuessService:
	"""
	A class to handle user guesses.

	Attributes:
		emojis (dict(str)): a dictionary holding the different emoji options
		word (str): the word to guess
		guess_str (str): a string representing all a user's guesses
		__guess_table(GuessesTable): an instance of the GuessesTable class

	Methods:
		add_guess(user_id): sends all user guesses to GuessesTable class to store
			in DB.
		convert_to_emoji(): converts all user guesses to an emoji representation
	"""

	def __init__(self):
		self.__guess_table = GuessesTable.GuessesTable()
		self.__word_service = WordService()
		self.emojis = {
			'correct_place': '🟩',
			'correct_letter': '🟨',
			'incorrect_letter': '⬛'
		}
		self.__query = db.session.query_property()

	@staticmethod
	def add_guess(user_id: int, guesses_str: str) -> Exception | None:
		"""
		Adds user's final guesses to database.

		Parameters:
			user_id (str): The id of the user making a guess
			guess_str (str): String containing all user guesses

		Raises:
			ValueError: if no guess has been made
		"""
		try:
			guess = Guess(
				user_id=user_id,
				guess_str=guesses_str
			)
			db.session.add(guess)
			db.session.commit()
			logging.info('New guess added')
		except Exception as e:
			e = f'Cannot add new guess to database for user {user_id}'
			logging.fatal(e)
			raise IOError(e)

	@staticmethod
	def get_guesses(user_id: int, guess_date: datetime) -> list[str] | None:
		guess = Guess.query.filter_by(guess_date=guess_date, user_id=user_id).first()
		if guess is None:
			e = f'Cannot retrieve guess from database for user {user_id} on {guess_date}'
			logging.warning(e)
			raise IOError(e)
		return guess.guess_str
			

	def convert_to_emoji(self, letter_scores: str) -> str:
		"""
		Converts a complete user guess to a string of emojis representing the
		accuracy of the guesses.

		Returns:
			emoji_str (str): The emoji representation of the guesses
		"""
		emoji_str = ''
		#TODO: replace with switch
		for letter_score in letter_scores:
			if letter_score == '\n':
				emoji_str = emoji_str + '\n'
			elif letter_score == '2':
				emoji_str = emoji_str + self.emojis['correct_place']
			elif letter_score == '1':
				emoji_str = emoji_str + self.emojis['correct_letter']
			elif letter_score == '0':
				emoji_str = emoji_str + self.emojis['incorrect_letter']
			else:
				raise ValueError(f'letter_scores contains unknown value ({letter_score}')
		return emoji_str

	def check_guess(self, guess):
		"""
		Checks the guess against the known word to assess the correctness.
		"""
		# I think this method can be written into front end to use caching with the word to prevent multiple requests
		# per user. This would otherwise overload the server if many guesses at once
		word = self.__word_service.get_word()
		letter_scores = '00000'
		for i in range(len(guess)):
			if guess[i] == word[i]: # type: ignore
				letter_scores = letter_scores[:i] + '2' + letter_scores[i + 1:]
			elif guess[i] in word:
				letter_scores = letter_scores[:i] + '1' + letter_scores[i + 1:]
		return self.convert_to_emoji(letter_scores)
