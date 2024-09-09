import datetime
from typing import Any

from src.service import guessService
from app import app
from src.utils.validations import Validators

guess_service = guessService.GuessService()


@app.route('/guess/add-guess/<string:guess>/<int:user_id>', methods=['POST'])
def add_guesses(guesses: str, user_id: int) -> Any:
	valid_word = Validators.final_guesses(guesses)
	if guesses != valid_word:
		response = app.make_response('Invalid final guesses string')
		response.status_code = 400
		return response

	response = guess_service.add_guess(user_id, guesses.lower())
	return app.make_response(f"Added user {user_id}'s guesses to database")


@app.route('/guess/check-single-guess/<string:guess>/', methods=['GET'])
def check_guess(guess: str) -> Any:
	valid_word = Validators.word(guess)
	if guess != valid_word:
		response = app.make_response('Invalid word')
		response.status_code = 400
		return response

	guess_score = guess_service.check_guess(guess.lower())
	return app.make_response(guess_score)


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
