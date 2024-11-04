from typing import Any

from flask import Blueprint
from src.service.userService import UserService
from app import app
from src.utils.validations import Validators

auth = Blueprint('user', __name__)
user_service = UserService()

@auth.route('/signup')
def signup():
	return 'Signup using url lol'

#TODO: This must be changed to use form fields and avoid plain text!!!
@auth.route('/signup/<str:email>/<str:username>', methods=['POST'])
def signup_post(email: str, username: str, password, str) -> Any:
	if len(username) > 20:
		response = app.make_response('Username too long')
		response.status_code = 401
		return response

	email_check = Validators.email(email)
	if email_check != email:
		response = app.make_response("Bad email")
		response.status_code = 401
		return response

	response = user_service.add_user(email, username, password)
	if response != 'Success':
		response = app.make_response("Failed to add user to database")
		response.status_code = 500

	return app.make_response('Scuccessfully added new user')

@auth.route('/login')
def login():
	return 'login'

@auth.route('/logout')
def logout():
	return 'logout'

	
