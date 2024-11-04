from typing import Any

from flask import Blueprint, make_response
from src.model.userModel import User
from src.service.userService import UserService
from src.utils.exceptions import DatabaseError
from src.utils.validations import Validators

auth = Blueprint('auth', __name__)
user_service = UserService()

@auth.route('/signup')
def signup():
	return 'Signup using url lol'

#TODO: This must be changed to use form fields and avoid plain text!!!
@auth.route('/send-signup/<string:email>/<string:username>/<string:password>', methods=['GET', 'POST'])
def signup_post(email: str, username: str, password: str) -> Any:
	if len(username) > 20:
		return make_response('Username too long', 400)

	if Validators.email(email) != email:
		return make_response('Bad email', 400)
	
	if User.query.filter_by(email=email).first():
		return make_response('Email already in use', 400)

	try:
		user_service.add_user(email, username, password)
		return make_response(f'Added user {username} successfully', 200)
	except DatabaseError:
		return make_response("Failed to add user to database", 500)
	
@auth.route('/login')
def login():
	return 'login'

@auth.route('/logout')
def logout():
	return 'logout'

	
