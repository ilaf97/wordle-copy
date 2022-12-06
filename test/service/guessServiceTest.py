import unittest
from src.service.guessService import GuessService
from src.service.wordService import WordService
from unittest.mock import MagicMock, patch


class TestGuessService(unittest.TestCase):
	__guess_service = GuessService()

	def test_convert_to_emoji(self):
		test_string = '01201\n20121'
		emoji_string = '⬛🟨🟩⬛🟨\n🟩⬛🟨🟩🟨'
		emoji_conversion = self.__guess_service.convert_to_emoji(test_string)
		self.assertEqual(emoji_string, emoji_conversion)

	@patch.object(WordService, 'get_word')
	def test_check_guess(self, mock_get_word):
		mock_get_word.return_value = 'river'
		test_word = 'dried'
		check_result = self.__guess_service.check_guess(test_word)
		self.assertEqual(check_result, '⬛🟨🟨🟩⬛')


if __name__ == '__main__':
	unittest.main()
