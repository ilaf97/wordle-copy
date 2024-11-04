from datetime import datetime
from typing import Any

from flask import Blueprint, make_response
from src.service import wordService
from src.service.wordService import WordService
from src.utils.exceptions import DatabaseError


word = Blueprint('word', __name__)
word_service = WordService()

@word.route('/get-word/', defaults={'date': datetime.strftime(datetime.now(), '%Y-%m-%d')}, methods=['GET'])
@word.route('/get-word/<string:date>', methods=['GET'])
def get_word(date: str) -> Any:
	try:
		word = word_service.get_word(datetime.strptime(date, "%Y-%m-%d").date())
		response = make_response(word)
		response.status_code = 200
	except DatabaseError as e:
		response = make_response(str(e))
		response.status_code = 500


	return f"<h1>{response.data}<h1>"
	#return app.make_response(word)

def add_word():
	pass
