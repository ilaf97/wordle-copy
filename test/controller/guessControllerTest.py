import unittest
from unittest.mock import patch
from src.controller.guessController import *
from src.service.wordService import WordService
from app import app


class TestGuessController(unittest.TestCase):

	def setUp(self) -> None:
		self.client = app.test_client()

	@patch.object(WordService, 'get_word')
	def test_check_guess(self, mock_get_word):
		mock_get_word.return_value = 'river'
		response = self.client.get('/guess/check-single-guess/dried/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			response.get_data(as_text=True),
			'⬛🟨🟨🟩⬛'
		)


if __name__ == '__main__':
	unittest.main()
