import unittest
from marshmallow import ValidationError
from src.utils.validations import Validators


class ValidatorTest(unittest.TestCase):
	__validators = Validators()

	def test_date_format_validator(self):
		date_correct = '2000-01-01'
		incorrect_cases = {
			'date_nonexistent': '2000-13-40',
			'date_wrong_chars': '1st January 2000',
			'date_empty': ''
		}
		self.assertTrue(self.__validators.date_format(date_correct).__repr__())
		for key, value in incorrect_cases.items():
			with self.assertRaises(ValidationError, msg=f'Test for {key} failed'):
				self.__validators.date_format(value)

	def test_word_validator(self):
		word_correct = 'hello'
		word_too_long = 'goodbye'
		word_too_short = 'hi'
		word_not_alpha = 'was\'nt'
		self.assertTrue(self.__validators.word(word_correct).__repr__())
		with self.assertRaises(ValidationError):
			self.__validators.word(word_too_long)
		with self.assertRaises(ValidationError):
			self.__validators.word(word_too_short)
		with self.assertRaises(ValidationError):
			self.__validators.word(word_not_alpha)

	def test_email_validator(self):
		email_correct = 'test@test.com'
		incorrect_cases = {
			'email_no_domain': 'test@test',
			'email_no_at': 'test.com',
			'email_empty': '',
			'email_domain_only': '.com'
		}
		self.assertEqual(email_correct, self.__validators.email(email_correct))
		for key, value in incorrect_cases.items():
			with self.assertRaises(ValidationError, msg=f'Test for {key} failed'):
				self.__validators.email(value)


if __name__ == '__main__':
	unittest.main()
