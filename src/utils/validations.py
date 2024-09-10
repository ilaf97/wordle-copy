import datetime
import string
from marshmallow import validate, ValidationError


class Validators:

	@staticmethod
	def date_format(date_str: str) -> ValidationError | str:
		validator = validate.Regexp(
			regex='^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$', # type: ignore
			error='Date format is incorrect: should be YYYY-MM-DD'
		)
		try:
			datetime.datetime.strptime(date_str, '%Y-%m-%d')
		except TypeError:
			return ValidationError('Date must be of type string')
		finally:
			return validator(date_str)

	@staticmethod
	def word(word: str) -> ValidationError | None:
		validator = validate.And(
			validate.Length(
				equal=5,
				error=f'Word not 5 characters: {word}'),
			validate.ContainsOnly(
				choices=string.ascii_lowercase,
				error=f'Word contains non-alphabetic characters: {word}'
			)
		)
		return validator(word)
	
	@staticmethod
	def final_guesses(guesses: str) -> ValidationError | None:
		validator = validate.And(
			validate.Length(
				equal=36,
				error=f'Guesses not 36 characters: {guesses}'),
			validate.ContainsOnly(
				choices=string.ascii_lowercase + '-',
				error=f'Word contains non-alphabetic characters: {guesses}'
			),
			validate.Regexp(
				regex='^[a-zA-Z]{5}-[a-zA-Z]{5}-[a-zA-Z]{5}-[a-zA-Z]{5}-[a-zA-Z]{5}-[a-zA-Z]{5}$',
				error='Guesses string not formatted corretly'
			)
		)
		return validator(guesses)

	@staticmethod
	def email(email: str) -> ValidationError | str:
		validator = validate.Email(error='Email is not in the correct format')
		return validator(email)
