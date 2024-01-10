from typing import Any
from src.service import wordService
from src.utils.validations import Validators


def word_route(app):

	word_service = wordService.WordService()

	@app.route('/word/get-word/<string:date>', methods=['GET'])
	def get_word(date: str) -> Any:
		check_date = Validators.date_format(date)
		# if check_date:
		# 	return app.make_response(check_date)

		word = word_service.get_word(date)
		if type(word) == Exception:
			return app.make_response(500)

		return app.make_response(word)
