import datetime
import re
from typing import Union
from marshmallow import validate, ValidationError


class Validators:

	@staticmethod
	def date_format(date_str: str) -> Union[None, ValidationError]:
		try:
			datetime.datetime.strptime(date_str, '%Y-%m-%d')
			return None
		except ValidationError:
			return ValidationError('Date format is incorrect: should be YYYY-MM-DD')

	@staticmethod
	def word(word: str) -> Union[None, ValidationError]:
		validator = validate.And(
			validate.Length(
				equal=5,
				error='Word must be 5 characters'),
			validate.Equal(
				comparable=True,
				error='Word contains non-alphabetic characters')
			(word.isalpha())
		)
		return validator(word)

	@staticmethod
	def email(email: str) -> Union[None, ValidationError]:
		validator = validate.Email(error='Email is not in the correct format')
		return validator(email)
