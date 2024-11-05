from src.model.wordModel import Word
from src import db

def _load_words() -> set[str]:
    words = set()
    with open('data/word_list.txt', 'r') as f:
        for word in f:
            words.add(word.strip().lower())
    return words

def _load_into_words_table(words):
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
    words = _load_words()
    _load_into_words_table(words)
