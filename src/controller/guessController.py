import datetime
from typing import Any
from flask import Blueprint, make_response

from src.service import guessService
from src.utils.exceptions import DatabaseError
from src.utils.validations import Validators

guess = Blueprint('guess', __name__)
guess_service = guessService.GuessService()

def _check_payload_guess_valid(guess: str) -> Any:
	valid_word = Validators.word(guess)
	if guess != valid_word:
		return make_response('Invalid word', 400)

@guess.route('/add-guess/<string:guess>/<int:user_id>', methods=['POST'])
def add_guesses(guesses: str, user_id: int) -> Any:
	try:
		guess_service.add_guesses(user_id, guesses.lower())
		return make_response(f"Added user {user_id}'s guesses to database", 200)
	except ValueError as e:
		return make_response(str(e), 400)
	except DatabaseError as e:
		return make_response(f"Failed to add user {user_id}'s guess to database", 500)

# This will be done client side too to reduce latency
@guess.route('/check-single-guess/<string:guess>/', methods=['GET'])
def check_guess(guess: str) -> Any:
	invalid_response  = _check_payload_guess_valid(guess)
	if invalid_response:
		return invalid_response

	guess_score = guess_service.check_individual_guess(guess.lower())
	return make_response(guess_score)

@guess.route('/check-all-guesses/<string:guesses>/', methods=['GET'])
def check_all_guesses(guesses: str) -> Any:
	scores = []
	individual_guesses = guesses.split('-')
	if len(individual_guesses) > 6:
		return make_response('Can only have a maximum of 6 guesses', 400)
	for guess in individual_guesses:
		invalid_response  = _check_payload_guess_valid(guess)
		if invalid_response:
			return invalid_response
		scores.append(guess_service.check_individual_guess(guess.lower()))
	return make_response('-'.join(scores), 200)

# Will be done client side
@guess.route('/guess/get-summary-for-date/<string:date>/<int:user_id>', methods=['GET'])
def get_all_guesses_emojis(date: str, user_id: int) -> Any:
	date_check = Validators.date_format(date)
	if date_check != date:
		return make_response("Invalid date", 400)

	guess_str = guess_service.get_guesses(user_id, datetime.datetime.strptime(date, '%Y-%m-%d'))
	if guess_str is None:
		return make_response(f'Cannot retrieve guesses for {user_id} on {date}', 500)
	else:
		return make_response(guess_str, 200)
