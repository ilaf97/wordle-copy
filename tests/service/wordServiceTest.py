import os
import unittest
from app import create_test_app
import src

from flask import Flask
from datetime import datetime, timedelta
from marshmallow import ValidationError
from src import db
from unittest.mock import MagicMock, patch
from src.model.wordModel import Word
from src.service.wordService import WordService
from tests.fixtures.load_fixture_data import get_fixtures, load_word_fixture_data
from src.utils.exceptions import DatabaseError

class TestWordService(unittest.TestCase):

	word_service = WordService()

	def setUp(self) -> None:
		app = create_test_app()
		self.fixture_data = get_fixtures('words')
		self.app_context = app.app_context()
		self.app_context.push()
		db.create_all()
		load_word_fixture_data(db)


	def tearDown(self) -> None:
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	@patch.object(src, 'db', db)
	@patch('random.randint')
	def test_select_valid_word(self, mock_randint):
		mock_randint.return_value = 1
		expected_word = self.fixture_data[0]['records'][0]['word']
		word_retrieved = self.word_service.select_random_word()
		self.assertIsNotNone(word_retrieved)
		if word_retrieved is not None:
			self.assertEqual(expected_word, word_retrieved.word)

	@patch.object(src, 'db', db)
	@patch('random.randint')
	def test_select_nonexistent_word_fails(self, mock_randint):
		mock_randint.return_value = 99999999
		with self.assertRaises(DatabaseError):
			word_retrieved = self.word_service.select_random_word()
			self.assertIsNone(word_retrieved)

	@patch.object(src, 'db', db)
	@patch('random.randint')
	def test_select_recent_word_fails(self, mock_randint):
		mock_randint.side_effect = [4, 3]
		expected_word = self.fixture_data[0]['records'][2]['word']
		# While loop in function under test will continue until valid word found
		word_retrieved: Word | None = self.word_service.select_random_word()
		self.assertIsNotNone(word_retrieved)
		if word_retrieved is not None:
			self.assertEqual(expected_word, word_retrieved.word)

	@patch.object(src, 'db', db)
	@patch('random.randint')
	def test_select_old_word_succeeds(self, mock_randint):
		mock_randint.return_value = 5
		expected_word = self.fixture_data[0]['records'][4]['word']
		word_retrieved: Word | None = self.word_service.select_random_word()
		self.assertIsNotNone(word_retrieved)
		if word_retrieved is not None:
			self.assertEqual(expected_word, word_retrieved.word)
	
				
	@patch.object(src, 'db', db)
	def test_add_valid_word(self):
		result = self.word_service.add_word('fleas')
		self.assertTrue(result)
		word_obj = db.session.query(Word).order_by(Word.id.desc()).first()
		self.assertIsNotNone(word_obj)
		self.assertEqual('fleas', word_obj.word) # type: ignore

	@patch.object(src, 'db', db)
	def test_add_invalid_word(self):
		with self.assertRaises(ValidationError):
			result = self.word_service.add_word('potato')
			self.assertFalse(result)
		word_obj = db.session.query(Word).order_by(Word.id.desc()).first()
		self.assertIsNotNone(word_obj)
		self.assertNotEqual('potato', word_obj.word) # type: ignore

	@patch.object(src, 'db', db)
	def test_add_duplicate_word(self):
		result = self.word_service.add_word('fleas')
		self.assertTrue(result)
		result = self.word_service.add_word('fleas')
		self.assertFalse(result)

	@patch.object(src, 'db', db)
	@patch('src.service.wordService.db.session.commit')
	@patch('src.service.wordService.db.session.add')
	def test_add_word_database_error(self, mock_db_add, mock_db_commit):
		exception = Exception('Bad operation')
		mock_db_commit.side_effect = exception
		with self.assertRaises(Exception):
			self.word_service.add_word('dream')
		mock_db_add.assert_called_once()

	@patch.object(src, 'db', db)
	@patch('src.service.wordService.Word.query')
	def test_get_word_valid_date(self, mock_query):
		# Mock a valid word object returned by the query
		word = 'clone'
		mock_word = MagicMock()
		mock_word.word = word
		mock_word.id = 1
		mock_query.filter_by.return_value.first.return_value = mock_word
		date = (datetime.now() - timedelta(days=1)).date()
		result = self.word_service.get_word(date)
		self.assertEqual(result, word)
		mock_query.filter_by.assert_called_once_with(selected_date=date)

	@patch('src.service.wordService.Word.query')
	@patch.object(WordService, '_handle_null_word_object')
	def test_get_word_valid_date_no_word_found(self, mock_handle_null_word_object, mock_query):
		mock_query.filter_by.return_value.first.return_value = None
		date = (datetime.now() - timedelta(days=1)).date()
		result = self.word_service.get_word(date)
		self.assertIsNone(result)
		mock_handle_null_word_object.assert_called_once_with('selected_date', date)
		mock_query.filter_by.assert_called_once_with(selected_date=date)

	@patch.object(WordService, '_handle_null_word_object')
	@patch.object(WordService, 'select_random_word')
	@patch('src.service.wordService.Word.query')
	def test_get_word_future_date(self, mock_query, mock_select_random_word, mock_handle_null_word_object):
		future_date = (datetime.now() + timedelta(days=1)).date()
		mock_query.filter_by.return_value.first.return_value = None
		mock_select_random_word.return_value = 'chair'
		result = self.word_service.get_word(future_date)
		mock_handle_null_word_object.assert_not_called()
		self.assertEqual(result, 'chair')
		mock_select_random_word.assert_called_once()

	@patch.object(WordService, 'select_random_word')
	@patch('src.service.wordService.Word.query')
	def test_get_word_no_date_passed(self, mock_query, mock_select_random_word):
		word = 'clone'
		mock_word = MagicMock()
		mock_word.word = word
		mock_word.id = 1
		mock_query.filter_by.return_value.first.return_value = 'chair'
		result = self.word_service.get_word()
		self.assertEqual(result, 'chair')
		mock_select_random_word.assert_not_called()

if __name__ == '__main__':
	unittest.main()
