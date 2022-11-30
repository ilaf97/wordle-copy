import datetime
import re
from typing import Union
from app import app
import logging


class Validators:

	@staticmethod
	def date_format(date_str: str) -> Union[None, ValueError]:
		try:
			datetime.datetime.strptime(date_str, '%Y-%m-%d')
			return None
		except ValueError:
			return ValueError('Date format is incorrect: should be YYYY-MM-DD')

	@staticmethod
	def word(word: str) -> Union[None, ValueError]:
		if len(word) != 5:
			return ValueError('Word not correct length: must be 5 characters')
		if not word.isalpha():
			return ValueError('Word contains non-alphabetical characters')
		return None

	@staticmethod
	def email(email: str) -> Union[None, ValueError]:
		pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
		if re.match(pat, email):
			return None
		return ValueError('Email is not in the correct format')
