import unittest

from flask_login import login_user
from src import db
from unittest.mock import patch
from app import create_test_app
from src.model.userModel import User
from src.service.userService import UserService
from src.service.wordService import WordService
from tests.fixtures.load_fixture_data import get_fixtures, load_user_fixture_data


class TestGuessController(unittest.TestCase):

	def setUp(self) -> None:
		app = create_test_app()
		self.guess_fixture_data = get_fixtures('guesses')
		self.user_fixture_data = get_fixtures('users')
		self.app_context = app.app_context()
		self.app_context.push()
		self.client = app.test_client()
		db.create_all()
		load_user_fixture_data(db)
		user_service = UserService()
		User.query.delete()
		user_to_add = self.user_fixture_data[0]['records'][1]
		user_service.add_user(
            email=user_to_add['email'],
            username=user_to_add['username'],
            password=user_to_add['password']
		)
		login_user(user_service.get_user_by_email(user_to_add['email']))

	def tearDown(self) -> None:
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

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
		response = self.client.get('/guess/check-single/no/')
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
