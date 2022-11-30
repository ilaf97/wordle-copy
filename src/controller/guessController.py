from typing import Any
from src.service import guessService
from app import app
from src.utils.validations import Validators


class GuessController:

	def __init__(self):
		self.__guess_service = guessService.GuessService()

	@app.route('guess/add-guess/<str:guess>', methods=['POST'])
	def add_guess(self, guess: str) -> Any:
		word_check = Validators.word(guess)
		if word_check:
			return app.make_response(word_check, 401)

		response = self.__guess_service.add_guess(guess)
		if response != 'Success':
			return app.make_response(response, 500)

		return app.make_response(response)

	@app.route('guess/check-single-guess/<str:guess>', methods=['GET'])
	def check_guess(self, guess: str) -> Any:
		word_check = Validators.word(guess)
		if word_check:
			return app.make_response(word_check, 401)

		guess_score = self.__guess_service.check_guess(guess)
		app.make_response(guess_score)

	@app.route('guess/get-summary-for-date/<str:date>/<int:user_id>', methods=['GET'])
	def get_all_guesses_emojis(self, date: str, user_id: int) -> Any:
		date_check = Validators.date_format(date)
		if date_check:
			return app.make_response(date_check, 401)

		guess_str = self.__guess_service.get_guesses(date, user_id)
		if type(guess_str) == Exception:
			return app.make_response(guess_str, 500)

		emoji_str = self.__guess_service.convert_to_emoji(guess_str)
		return app.make_response(emoji_str)



