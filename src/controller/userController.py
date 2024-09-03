from typing import Any
from src.service import userService
from app import app
from src.utils.validations import Validators


class UserController:

	def __init__(self):
		self.__user_service = userService.UserService()

	@app.route('user/add-user/<str:email>/<str:username>', methods=['POST'])
	def add_user(self, email: str, username: str) -> Any:
		if len(username) > 20:
			response = app.make_response('Username too long')
			response.status_code = 401
			return response

		email_check = Validators.email(email)
		if email_check != email:
			response = app.make_response("Bad email")
			response.status_code = 401
			return response

		response = self.__user_service.add_user(email, username)
		if response != 'Success':
			#TODOL this should be handled by the service
			response = app.make_response("Failed to add user to database")
			response.status_code = 500

		return app.make_response('Scuccessfully added new user')


