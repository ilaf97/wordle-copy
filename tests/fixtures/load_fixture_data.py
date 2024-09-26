from flask import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from src.model.guessModel import Guess
from src.model.wordModel import Word


def get_fixtures(filename: str) -> dict:
    with open(f'tests/fixtures/{filename}.json') as f:
        return json.load(f)
    

def load_guess_fixture_data(db: SQLAlchemy) -> None:
    fixtures = get_fixtures('guesses')
    for fixture in fixtures:
        # Ensure correct table always read in
        if fixture['table'] == 'guess':
            for record in fixture['records']:
                guess = Guess(
                    guess_str=record['guess_str'],
                    user_id=record['user_id'],
                )
                guess.guess_date = datetime.strftime(record['guess_date'], '%Y-%m-%d')
                db.session.add(guess)
                db.session.commit()


def load_word_fixture_data(db: SQLAlchemy) -> None:
    fixtures = get_fixtures('words')
    for fixture in fixtures:
        # Ensure corrext table always read in
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

