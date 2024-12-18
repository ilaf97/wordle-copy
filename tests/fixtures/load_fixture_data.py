from flask import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from src.model.userModel import User
from src.model.guessModel import Guess
from src.model.wordModel import Word


def get_fixtures(filename: str) -> dict:
    with open(f'tests/fixtures/{filename}.json') as f:
        return json.load(f)
    

def load_guess_fixture_data(db: SQLAlchemy) -> None:
    fixtures = get_fixtures('guesses')
    for fixture in fixtures:
        if fixture['table'] == 'guess':
            for record in fixture['records']:
                guess = Guess(
                    guess_str=record['guess_str'],
                    user_id=record['user_id'],
                    guess_date=record['guess_date']
                )
                guess.guess_date = datetime.strptime(record['guess_date'], '%Y-%m-%d')
                db.session.add(guess)
                db.session.commit()


def load_word_fixture_data(db: SQLAlchemy) -> None:
    fixtures = get_fixtures('words')
    for fixture in fixtures:
        if fixture['table'] == 'word':
            for record in fixture['records']:
                word = Word(
                    word=record['word'],
                )
                selected_date = record['selected_date']
                if selected_date == 'RECENT':
                    selected_date = datetime.now()
                if selected_date == 'OLD':
                    selected_date = datetime(2000, 1, 1)
                word.selected_date = selected_date
                db.session.add(word)
                db.session.commit()

def load_user_fixture_data(db: SQLAlchemy) -> None:
    fixtures = get_fixtures('users')
    for fixture in fixtures:
        if fixture['table'] == 'user':
            for record in fixture['records']:
                user = User(
                    username=record['username'],
                    email=record['email'],
                    password=record['password']
                )
                db.session.add(user)
                db.session.commit()

