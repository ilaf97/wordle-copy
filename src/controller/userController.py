from typing import Any

from flask import Blueprint, make_response, redirect, render_template, request
from flask_login import login_required, login_user, logout_user
from src.model.userModel import User
from src.service.userService import UserService
from src.utils.exceptions import DatabaseError
from src.utils.validations import Validators

auth = Blueprint('auth', __name__)
user_service = UserService()

@auth.route('/signup', methods=['GET'])
def signup():
	return render_template('signup.html')

#TODO: This must be changed to use form fields and avoid plain text!!!
@auth.route('/signup', methods=['POST'])
def signup_post() -> Any:
	email = request.form.get('email')
	username = request.form.get('username')
	password = request.form.get('password')
	if any(field is None for field in (email, username, password)):
		return make_response('Missing values', 400)
	
	if username == 'admin':
		return make_response("'admin' is a reserved username. Please choose another", 400)

	if len(username) > 20: # type: ignore
		return make_response('Username too long', 400)

	if Validators.email(email) != email: # type: ignore
		return make_response('Bad email', 400)
	
	#This should not be in the controller
	if user_service.get_user_by_email(email): # type: ignore
		users = User.query.all()
		emails_in_use = [user.email for user in users]
		return make_response(f'Email already in use. Users: {'\n'.join(emails_in_use)}', 400)

	try:
		user_service.add_user(email, username, password) # type: ignore
		return render_template('login.html')
	except DatabaseError:
		return make_response("Failed to add user to database", 500)
		
	
@auth.route('/login', methods=['GET'])
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False
	if any(field is None for field in (email, password)):
		return make_response('Missing values', 400)
	
	check_user_credentails = user_service.check_credentials(email, password) # type: ignore
	if not check_user_credentails:
		return make_response('User not found', 401)
	login_user(user_service.get_user_by_email(email), remember=remember) # type: ignore
	return render_template('guesser.html')

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return render_template('login.html')


	
