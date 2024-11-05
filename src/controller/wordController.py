from datetime import datetime
import os
from typing import Any

from flask import Blueprint, make_response, render_template, request
from flask_login import current_user
from src.service import wordService
from src.service.wordService import WordService
from src.utils.exceptions import DatabaseError
from utils.validations import Validators


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

@word.route('/add-word', methods=['GET'])
def add_word():
	if current_user.email != os.environ['ADMIN_EMAIL']:
		return make_response("User not authorised to add words", 403)
	return render_template('add_word.html')

@word.route('/add-word', methods=['POST'])
def add_word_post():
	if current_user.email != os.environ['ADMIN_EMAIL']:
		return make_response("User not authorised to add words", 403)
	word = request.form.get('word')
	valid_word = Validators.word(word) # type: ignore
	if valid_word:
		word_service.add_word(word) # type: ignore
		return make_response(f"Word '{word}' added successfully")
	return make_response(f"Word '{word}' is not valid", 400)
	
