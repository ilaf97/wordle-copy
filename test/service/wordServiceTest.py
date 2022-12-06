import unittest
from unittest.mock import patch
from src.service.wordService import WordService
from freezegun import freeze_time
from test.test_data import test_word_list, empty_word_list


class TestWordService(unittest.TestCase):
	__word_service = WordService()
	mock_word_list = 'test/data/test_word_list.txt'

	def test_get_current_date(self):
		with freeze_time('2022-01-01'):
			test_date = self.__word_service._WordService__get_current_date_str()
			self.assertEqual(test_date, '2022-01-01')

	@patch.object(__word_service, 'word_list', test_word_list)
	def test_count_input_lines(self):
		test_count = self.__word_service._WordService__count_input_lines()
		self.assertEqual(test_count, 10)

	@patch.object(__word_service, 'word_list', empty_word_list)
	def test_count_empty_file(self):
		test_count = self.__word_service._WordService__count_input_lines()
		self.assertEqual(0, test_count)
		with self.assertLogs() as captured:
			self.__word_service._WordService__count_input_lines()
			self.assertEqual(
				captured.records[0].getMessage(),
				'No words in word_list.txt'
			)

	@patch.object(__word_service, 'word_list', '')
	def test_select_object(self):
		with self.assertLogs() as captured:
			self.__word_service.select_word()
			self.assertEqual(
				captured.records[0].getMessage(),
				'Could not open word_list.txt file'
			)


if __name__ == '__main__':
	unittest.main()
