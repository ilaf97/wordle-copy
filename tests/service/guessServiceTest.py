from datetime import datetime, timedelta
import os
import unittest

from flask import Flask
from marshmallow import ValidationError
from src import db
import src
from src.model.guessModel import Guess
from src.service.guessService import GuessService
from src.service.wordService import WordService
from unittest.mock import MagicMock, patch

from tests.fixtures.load_fixture_data import get_fixtures, load_guess_fixture_data


class TestGuessService(unittest.TestCase):

	guess_service = GuessService()
	test_guesses_str = 'dream-fleas-tests-chuck-diver-quack'


	def setUp(self) -> None:
		self.app = Flask(__name__)
		self.app.config['TESTING'] = True
		self.app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['TEST_DATABASE_URL']
		db.init_app(self.app)
		self.fixture_data = get_fixtures('guesses')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		load_guess_fixture_data(db)


	def tearDown(self) -> None:
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_convert_to_emoji_correct_conversion(self):
		test_string = '01201-20121'
		emoji_string = '⬛🟨🟩⬛🟨-🟩⬛🟨🟩🟨'
		emoji_conversion = self.guess_service.convert_to_emoji(test_string)
		self.assertEqual(emoji_string, emoji_conversion)

	def test_convert_to_emoji_incorrect_conversion(self):
		test_string = '00000-01201'
		emoji_string = '⬛🟨🟩⬛🟨-🟩⬛🟨🟩🟨'
		emoji_conversion = self.guess_service.convert_to_emoji(test_string)
		self.assertNotEqual(emoji_string, emoji_conversion)

	def test_convert_to_emoji_with_invalid_number_raises_exception(self):
		test_string = '00003-01201'
		with self.assertRaises(ValueError) as e:
			self.guess_service.convert_to_emoji(test_string)

		self.assertEqual(str(e.exception), 'letter scores can only be 1, 2 or 3: found unknown value 3')

	def test_convert_to_emoji_with_invalid_char_raises_exception(self):
		test_string = '!@£$%\-^&*(?'
		with self.assertRaises(ValueError) as e:
			self.guess_service.convert_to_emoji(test_string)

		self.assertEqual(str(e.exception), 'letter scores can only be 1, 2 or 3: found unknown value !')

	@patch.object(WordService, 'get_word')
	def test_check_guess(self, mock_get_word):
		mock_get_word.return_value = 'river'
		test_word = 'dried'
		check_result = self.guess_service.check_individual_guess(test_word)
		self.assertEqual(check_result, '01120')

	#TODO: add the body for the below tests once database fixtures have been added

	@patch.object(src, 'db', db)
	def test_add_valid_guesses(self):
		result = self.guess_service.add_guesses(99999, self.test_guesses_str)
		self.assertTrue(result)
		guess_obj = db.session.query(Guess).order_by(Guess.id.desc()).first()
		self.assertIsNotNone(guess_obj)
		self.assertEqual(self.test_guesses_str, guess_obj.guess_str) # type: ignore

	@patch.object(src, 'db', db)
	def test_add_invalid_guesses(self):
		with self.assertRaises(ValidationError):
			result = self.guess_service.add_guesses(99999, "this is an invalid guess string")
			self.assertFalse(result)

	@patch.object(src, 'db', db)
	def test_add_invalid_user_id(self):
		with self.assertRaises(Exception):
			self.guess_service.add_guesses(-1, self.test_guesses_str)

	@patch.object(src, 'db', db)
	@patch('src.service.guessService.db.session.commit')
	@patch('src.service.guessService.db.session.add')
	def test_add_guess_database_error(self, mock_db_add, mock_db_commit):
		exception = Exception('Bad operation')
		mock_db_commit.side_effect = exception
		with self.assertRaises(Exception):
			self.guess_service.add_guesses(99999, self.test_guesses_str)
		mock_db_add.assert_called_once()

	@patch.object(src, 'db', db)
	@patch('src.service.guessService.Guess.query')
	def test_get_guess_valid_user_id(self, mock_query):
		guess = 'clone-dream-pious-cream-scran'
		mock_guess = MagicMock()
		mock_guess.guess_str = guess
		mock_guess.id = 1
		mock_guess.user_id = 1
		mock_query.filter_by.return_value.first.return_value = mock_guess
		date = datetime.now() - timedelta(days=1)
		result = self.guess_service.get_guesses(user_id=1, guess_date=date) # type: ignore
		self.assertEqual(result, guess) # type: ignore
		mock_query.filter_by.assert_called_once_with(user_id=1, guess_date=date)
		
	@patch.object(src, 'db', db)
	@patch('src.service.guessService.Guess.query')
	def test_get_guess_invalid_user_id(self, mock_query):
		guess = 'clone-dream-pious-cream-scran'
		mock_guess = MagicMock()
		mock_guess.guess_str = guess
		mock_guess.id = 1
		mock_guess.user_id = -1
		mock_query.filter_by.return_value.first.return_value = mock_guess
		date = datetime.now() - timedelta(days=1)
		with self.assertRaises(Exception):
			result = self.guess_service.get_guesses(user_id=-1, guess_date=date) # type: ignore

	def test_get_guesses_database_error(self):
		pass


if __name__ == '__main__':
	unittest.main()
