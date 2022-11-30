from src.service import guessService
from flask import Flask, request
from app import app
import logging


class GuessController:

	def __init__(self):
		self.__guess_service = guessService.GuessService()

	@app.route('guess/get-summary-for-date', methods=['GET'])
	def get_all_guesses_emojis(self):
		date = request.args.get('date')

		return self.__guess_service.convert_to_emoji(guess_str)

	@app.route('guess/check-single-guess', methods=['GET'])
	async def check_guess(self):
		guess_str = request.args.get('guess')
		if len(guess_str) != 5:
			app.make_response('Guess must be 5 chars only',  401)
		else:
			guess_score = self.__guess_service.check_guess(guess_str)
			app.make_response(guess_score)


