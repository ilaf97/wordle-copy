from resources import GuessesTable


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

	def add_guess(self, user_id: str):
		"""
		Adds user's final guesses to database.

		Parameters:
			user_id (str): The id of the user making a guess

		Raises:
			ValueError: if no guess has been made
		"""
		if len(self.guess_str) < 5:
			raise ValueError("Guess string is empty")
		else:
			guess_list = self.guess_str.split('\n')
			self.__guess_table.add_user_guess(user_id, guess_list)

	def retrieve_word(self):
		# Implement getter from database
		# Put in word service?
		pass

	def handle_guess(self, guess: str):
		"""
		Handles a user's guess.

		Parameters:
			guess (str): a single, individual guess

		Raises:
			ValueError: if user attempts to make more than 6 guesses
		"""
		if self.guess_num < 6:
			self.__check_guess(guess)
		else:
			raise IndexError("You cannot guess more than 6 times!")

	def convert_to_emoji(self) -> str:
		"""
		Converts a complete user guess to a string of emojis representing the
		accuracy of the guesses.

		Returns:
			emoji_str (str): The emoji representation of the guesses
		"""
		emoji_str = ''
		for letter_score in self.guess_str:
			if letter_score == '\n':
				emoji_str = emoji_str + '\n'
			elif letter_score == 2:
				emoji_str = emoji_str + self.emojis['correct_place']
			elif letter_score == 1:
				emoji_str = emoji_str + self.emojis['correct_letter']
			else:
				emoji_str = emoji_str + self.emojis['incorrect_letter']
		return emoji_str

	def __check_guess(self, guess):
		"""
		Checks the guess against the known word to assess the correctness.
		"""
		letter_scores = '00000'
		for i in range(len(guess)):
			if guess[i] == self.word[i]:
				letter_scores = letter_scores[:i] + 2 + letter_scores[i + 1:]
			elif guess[i] in self.word:
				letter_scores = letter_scores[:i] + 1 + letter_scores[i + 1:]
		self.guess_str = self.guess_str + letter_scores + '\n'
		self.guess_num += 1
