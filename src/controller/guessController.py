from typing import Any
from src.service import guessService
from app import app
from src.utils.validations import Validators

guess_service = guessService.GuessService()


@app.route('/guess/add-guess/<string:guess>', methods=['POST'])
def add_guesses(guess: str) -> Any:
	word_check = Validators.word(guess)
	if word_check != guess:
		return app.make_response(word_check)

	response = guess_service.add_guess(guess.lower())
	if response != 'Success':
		return app.make_response(response)

	return app.make_response(response)


@app.route('/guess/check-single-guess/<string:guess>/', methods=['GET'])
def check_guess(guess: str) -> Any:
	word_check = Validators.word(guess)
	if word_check != guess:
		return app.make_response(word_check)

	guess_score = guess_service.check_guess(guess.lower())
	return app.make_response(guess_score)


@app.route('/guess/get-summary-for-date/<string:date>/<int:user_id>', methods=['GET'])
def get_all_guesses_emojis(date: str, user_id: int) -> Any:
	date_check = Validators.date_format(date)
	if date_check != date:
		return app.make_response(date_check)

	guess_str = guess_service.get_guesses(date, user_id)
	if type(guess_str) == Exception:
		return app.make_response(guess_str)

	emoji_str = guess_service.convert_to_emoji(guess_str)
	return app.make_response(emoji_str)
