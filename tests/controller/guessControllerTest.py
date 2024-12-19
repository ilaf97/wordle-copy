import unittest
from unittest.mock import patch
from src.service.wordService import WordService
from app import app
from tests.fixtures.load_fixture_data import get_fixtures


class TestGuessController(unittest.TestCase):

	def setUp(self) -> None:
		self.client = app.test_client()
		self.fixture_data = get_fixtures('guesses')

	@patch.object(WordService, 'get_word')
	def test_check_guess_correct(self, mock_get_word):
		mock_get_word.return_value = 'river'
		response = self.client.get('/guess/check-single/river/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			response.get_data(as_text=True),
			'🟩🟩🟩🟩🟩'
		)

	@patch.object(WordService, 'get_word')
	def test_check_guess_partially_correct(self, mock_get_word):
		mock_get_word.return_value = 'river'
		response = self.client.get('/guess/check-single/dried/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			response.get_data(as_text=True),
			'⬛🟨🟨🟩⬛'
		)

	@patch.object(WordService, 'get_word')
	def test_check_guess_incorrect(self, mock_get_word):
		mock_get_word.return_value = 'river'
		response = self.client.get('/guess/check-single/blood/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			response.get_data(as_text=True),
			'⬛⬛⬛⬛⬛'
		)

	def test_check_guess_invalid_word(self):
		response = self.client.get('/guess/check-single/no')
		self.assertEqual(response.status_code, 400)

	#TODO: add the body for the below tests once database fixtures have been added

	def test_get_all_guesses_emojis_valid_date(self):
		pass
		
	def test_get_all_guesses_emojis_invalid_date(self):
		pass

	def test_get_all_guesses_emojis_server_error(self):
		pass

	def test_add_guesses_valid_format(self):
		pass

	def test_add_guess_invalid_format(self):
		pass
		

if __name__ == '__main__':
	unittest.main()
