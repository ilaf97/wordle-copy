import logging
from resources import GuessesTable
from datetime import datetime
from src.model.guessModel import Guess
from src.service.wordService import WordService
from src import db
from src.utils.validations import Validators


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

	@staticmethod
	def add_guesses(user_id: int, guesses_str: str) -> None:
		"""
		Adds user's final guesses to database.

		Parameters:
			user_id (str): The id of the user making a guess
			guess_str (str): String containing all user guesses

		Raises:
			ValueError: if no guess has been made
		"""
		valid_word = Validators.final_guesses(guesses_str)
		if guesses_str != valid_word:
			raise ValueError(f'Invalid guess string {guesses_str}')
		if user_id <= 0:
			raise ValueError(f'Invlaid user_id of {user_id}')
		
		guess = Guess(
			user_id=user_id,
			guess_str=guesses_str
		)
		db.session.add(guess)
		db.session.commit()
		logging.info('New guess added')


	@staticmethod
	def get_guesses(user_id: int, guess_date: datetime) -> list[str] | None:
		if guess_date > datetime.now():
			raise ValueError('guess_date cannot be in future')
		if user_id <=0:
			raise ValueError('user_id must be positive integer')

		guess = Guess.query.filter_by(guess_date=guess_date, user_id=user_id).first()
		if guess is None:
			e = f'Cannot retrieve guess from database for user {user_id} on {guess_date}'
			logging.warning(e)
			raise IOError(e)
		return guess.guess_str
			

	def convert_to_emoji(self, letter_scores: str) -> str:
		"""
		Converts a complete user guess to a string of emojis representing the
		accuracy of the guess.

		Returns:
			emoji_str (str): The emoji representation of the guess
		"""
		# Add to front end to speed-up requests?
		emoji_str = ''
		for letter_score in letter_scores:
			match letter_score:
				case '-':
					emoji_str = emoji_str + '-'
				case '2':
					emoji_str = emoji_str + self.emojis['correct_place']
				case '1':
					emoji_str = emoji_str + self.emojis['correct_letter']
				case '0':
					emoji_str = emoji_str + self.emojis['incorrect_letter']
				case _:
				#TODO: possibly implement a exception class instead of writing errors inline
					raise ValueError(f'letter scores can only be 1, 2 or 3: found unknown value {letter_score}')
		return emoji_str

	def check_individual_guess(self, guess) -> str:
		"""
		Checks the latest guess against the known word to assess the correctness.
		"""
		# I think this method can be written into front end to use caching with the word to prevent multiple requests
		# per user. This would otherwise overload the server if many guesses at once
		word = self.__word_service.get_word()
		letter_scores = ["0", "0", "0", "0", "0"]
		for i in range(len(guess)):
			if guess[i] == word[i]: # type: ignore
				letter_scores[i] = "2"
			elif guess[i] in word:
				letter_scores[i] = "1"
			elif guess[i] not in word:
				letter_scores[i] = "0"

		letter_scores_str = ''.join(letter_scores)
		return letter_scores_str
