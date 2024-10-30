from datetime import datetime
from typing import Any
from src.service import wordService



def word_route(app):
	word_service = wordService.WordService()

	@app.route('/word/get-word/', defaults={'date': datetime.strftime(datetime.now(), '%Y-%m-%d')})
	@app.route('/word/get-word/<string:date>', methods=['GET'])
	def get_word(date: str) -> Any:
		try:
			word = word_service.get_word(datetime.strptime(date, "%Y-%m-%d"))
			response = app.make_response(word)
			response.status_code = 200
		except IOError as e:
			response = app.make_response(str(e))
			response.status_code = 500


		return f"<h1>{response.data}<h1>"
		#return app.make_response(word)
