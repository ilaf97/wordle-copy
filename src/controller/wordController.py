from typing import Any
from src.service import wordService
from app import app
from src.utils.validations import Validators


class WordController:

	def __init__(self):
		self.__word_service = wordService.WordService()

	@app.route('word/get-word/<str:date>', methods=['GET'])
	def get_word(self, date: str) -> Any:
		check_date = Validators.date_format(date)
		if check_date:
			return app.make_response(check_date, 401)

		word = self.__word_service.get_word(date)
		if type(word) == Exception:
			return app.make_response(word, 500)

		return app.make_response(word)
