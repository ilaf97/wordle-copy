from typing import Any
from src.service import userService
from app import app
from src.utils.validations import Validators


class UserController:

	def __init__(self):
		self.__user_service = userService.UserService()

	@app.route('user/add-user/<str:email>/<str:username>', methods=['POST'])
	def add_user(self, email: str, username: str) -> Any:
		if username > 20:
			app.make_response('Username too long', 401)
		email_check = Validators.email(email)
		if email_check:
			return app.make_response(email_check, 401)

		response = self.__user_service.add_user(email, username)
		if response != 'Success':
			return app.make_response(response, 500)

		return app.make_response(response)

	#TODO: implement update_email endpoint

