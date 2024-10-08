import unittest
from unittest.mock import patch
from src.service.wordService import WordService
from freezegun import freeze_time
from tests.fixtures import test_word_list, empty_word_list

#TODO: create database fixture to test CRUD methods in service work

class TestWordService(unittest.TestCase):

	word_service = WordService()

	def test_get_current_date(self):
		with freeze_time('2022-01-01'):
			test_date = self.word_service.get_current_date_str()
			self.assertEqual(test_date, '2022-01-01')

	@patch.object(word_service, 'word_list', test_word_list)
	def test_count_input_lines(self):
		test_count = self.word_service._count_input_lines()
		self.assertEqual(test_count, 10)

	@patch.object(word_service, 'word_list', empty_word_list)
	def test_count_empty_file(self):
		test_count = self.word_service._count_input_lines()
		self.assertEqual(0, test_count)
		with self.assertLogs() as captured:
			self.word_service._count_input_lines()
			self.assertEqual(
				captured.records[0].getMessage(),
				'No words in word_list.txt'
			)

	@patch.object(word_service, 'word_list', '')
	def test_select_object(self):
		with self.assertLogs() as captured:
			self.word_service.select_word()
			self.assertEqual(
				captured.records[0].getMessage(),
				'Could not open word_list.txt file'
			)

	def test_add_valid_word(self):
		pass

	def test_add_invalid_word(self):
		pass

	def test_add_word_successfully(self):
		pass

	def test_add_word_database_error(self):
		pass

	def test_get_word(self):
		pass

	def test_get_word_database_error(self):
		pass



if __name__ == '__main__':
	unittest.main()
