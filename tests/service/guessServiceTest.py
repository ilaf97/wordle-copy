import unittest
from src.service.guessService import GuessService
from src.service.wordService import WordService
from unittest.mock import patch


class TestGuessService(unittest.TestCase):

	def setUp(self) -> None:
		self.guess_service = GuessService()

	def test_convert_to_emoji_correct_conversion(self):
		test_string = '01201\n20121'
		emoji_string = '⬛🟨🟩⬛🟨\n🟩⬛🟨🟩🟨'
		emoji_conversion = self.guess_service.convert_to_emoji(test_string)
		self.assertEqual(emoji_string, emoji_conversion)

	def test_convert_to_emoji_incorrect_conversion(self):
		test_string = '00000\n01201'
		emoji_string = '⬛🟨🟩⬛🟨\n🟩⬛🟨🟩🟨'
		emoji_conversion = self.guess_service.convert_to_emoji(test_string)
		self.assertNotEqual(emoji_string, emoji_conversion)

	def test_convert_to_emoji_with_invalid_number_raises_exception(self):
		test_string = '00003\n01201'
		with self.assertRaises(ValueError) as e:
			self.guess_service.convert_to_emoji(test_string)

		self.assertEqual(str(e.exception), 'letter scores can only be 1, 2 or 3: found unknown value 3')

	def test_convert_to_emoji_with_invalid_char_raises_exception(self):
		test_string = '!@£$%\n^&*(?'
		with self.assertRaises(ValueError) as e:
			self.guess_service.convert_to_emoji(test_string)

		self.assertEqual(str(e.exception), 'letter scores can only be 1, 2 or 3: found unknown value !')

	@patch.object(WordService, 'get_word')
	def test_check_guess(self, mock_get_word):
		mock_get_word.return_value = 'river'
		test_word = 'dried'
		check_result = self.guess_service.check_guess(test_word)
		self.assertEqual(check_result, '⬛🟨🟨🟩⬛')

	#TODO: add the body for the below tests once database fixtures have been added

	def test_add_guess(self):
		pass

	def test_add_guess_database_error(self):
		pass

	def test_get_guesses(self):
		pass

	def test_get_guesses_database_error(self):
		pass


if __name__ == '__main__':
	unittest.main()
