import datetime
import logging
from typing import Any

from src.service import guessService
from src.utils.validations import Validators


def guess_route(app):

	guess_service = guessService.GuessService()

	def _check_payload_guess_valid(guess: str) -> Any:
		valid_word = Validators.word(guess)
		if guess != valid_word:
			response = app.make_response('Invalid word')
			response.status_code = 400
			return response


	@app.route('/guess/add-guess/<string:guess>/<int:user_id>', methods=['POST'])
	def add_guesses(guesses: str, user_id: int) -> Any:
		try:
			guess_service.add_guesses(user_id, guesses.lower())
			response = app.make_response(f"Added user {user_id}'s guesses to database")
			response.status_code = 200
		except ValueError as e:
			response = app.make_response(str(e))
			response.status_code = 400
		except Exception as e:
			response = app.make_response(f"Failed to add user {user_id}'s guess to database. Error: {str(e)}")
			response.status_code = 500
		finally:
			return response
 
	# This will be done client side too to reduce latency
	@app.route('/guess/check-single-guess/<string:guess>/', methods=['GET'])
	def check_guess(guess: str) -> Any:
		invalid_response  = _check_payload_guess_valid(guess)
		if invalid_response:
			return invalid_response

		guess_score = guess_service.check_individual_guess(guess.lower())
		return app.make_response(guess_score)
	
	@app.route('/guess/check-all-guesses/<string:guesses>/', methods=['GET'])
	def check_all_guesses(guesses: str) -> Any:
		scores = ''
		individual_guesses = guesses.split('-')
		for guess in individual_guesses:
			invalid_response  = _check_payload_guess_valid(guess)
			if invalid_response:
				return invalid_response
			scores += '-' + (guess_service.check_individual_guess(guess.lower()))
		return scores

	# Will be done client side
	@app.route('/guess/get-summary-for-date/<string:date>/<int:user_id>', methods=['GET'])
	def get_all_guesses_emojis(date: str, user_id: int) -> Any:
		date_check = Validators.date_format(date)
		if date_check != date:
			response = app.make_response("Invalid date")
			response.status_code = 400
			return response

		guess_str = guess_service.get_guesses(user_id, datetime.datetime.strptime(date, '%Y-%m-%d'))
		if guess_str is None:
			response = app.make_response(f'Cannot retrieve guesses for {user_id} on {date}')
			response.status_code = 500
			return response
		else:
			return app.make_response(guess_str)
