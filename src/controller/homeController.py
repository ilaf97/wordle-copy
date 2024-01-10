# This file is a test homepage
def home_route(app):
	@app.route('/')
	def home() -> str:
		return "<h1>Welcome to Word Guesser!</h1>"