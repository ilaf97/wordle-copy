import os
from src.model.userModel import User
from src.model.wordModel import Word
from src import db

def load_words() -> set[str]:
    words = set()
    with open('data/word_list.txt', 'r') as f:
        for word in f:
            words.add(word.strip().lower())
    return words

def load_into_words_table(words):
    Word.query.delete()
    for word in words:
        word_obj = Word(word=word)
        db.session.add(word_obj)

    try:
        db.session.commit()
        print('Successfully loaded words into table')
    except Exception as e:
        print(f'Failed to add words: {e}')


def run_words_etl():
    words = load_words()
    load_into_words_table(words)

def clear_users():
    User.query.delete()
    db.session.commit()

def create_admin_user():
    admin_user = User(
        username='admin',
        email=['ADMIN_EMAIL'],
        password=os.environ['ADMIN_PASSWORD']
    )
    db.session.add(admin_user)