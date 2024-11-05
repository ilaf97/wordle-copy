from model.guessModel import Guess

def clear_all_guesses():
    Guess.query.delete()
