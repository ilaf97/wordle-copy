import datetime
import string
from typing import Union
from marshmallow import validate, ValidationError


class Validators:

	@staticmethod
	def date_format(date_str: str) -> Union[None, ValidationError]:
		validator = validate.Regexp(
			regex='^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$',
			error='Date format is incorrect: should be YYYY-MM-DD'
		)
		try:
			datetime.datetime.strptime(date_str, '%Y-%m-%d')
		except TypeError:
			return ValidationError('Date must be of type string')
		except ValueError:
			pass
		finally:
			return validator(date_str)

	@staticmethod
	def word(word: str) -> Union[None, ValidationError]:
		validator = validate.And(
			validate.Length(
				equal=5,
				error='Word must be 5 characters'),
			validate.ContainsOnly(
				choices=string.ascii_lowercase,
				error='Word contains non-alphabetic characters'
			)
		)
		return validator(word)

	@staticmethod
	def email(email: str) -> Union[str, ValidationError]:
		validator = validate.Email(error='Email is not in the correct format')
		return validator(email)
