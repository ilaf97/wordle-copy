import random
import logging
from typing import Any

from sqlalchemy import func
from src.model.wordModel import Word
from src.utils.validations import Validators
from datetime import datetime, timedelta
from src import db


class WordService:

    def _handle_null_word_object(self, field: str, field_value: Any):
        e = f'Cannot retrieve word from database for {field} with value {str(field_value)}'
        logging.warning(e)
        raise IOError(e)

    def add_word(self, word: str) -> bool:
        word_validation_error = Validators.word(word)
        if word_validation_error != word:
            logging.warning(word_validation_error)
            return False
        else:
            try:
                word_model = Word(word=word)
                db.session.add(word_model)
                db.session.commit()
                logging.info('New word added')
                return True
            except Exception as e:
                logging.error('Cannot add new word to database')
                logging.error(e)
                return False

    def get_word(self, date: str = '') -> str | None:
        if date != '' and datetime.strptime(date, '%Y-%m-%d') < datetime.now():
            word_object = Word.query.filter_by(date=Word.selected_date).first()
            if word_object is None:
                self._handle_null_word_object("selected_date", date)
                return
            return word_object.word
        return self.select_random_word()
        
    def select_random_word(self) -> str | None:
        max_id = db.session.query(func.max(Word.id)).scalar()
        i = 0
        while i < 50:
            id_to_select = random.randint(1 , max_id)
            word_object = db.session.query(Word).filter(Word.id==id_to_select).first()
            if word_object is None:
                self._handle_null_word_object("id", id_to_select)
                # Return as this indicates data issue
                return

            three_months_ago = datetime.now() - timedelta(weeks=13)
            if word_object.selected_date is None or word_object.selected_date < three_months_ago:
                return word_object.word
            i += 1
        
    @staticmethod
    def get_current_date_str() -> str:
        curr_date = datetime.now()
        return datetime.strftime(curr_date, '%Y-%m-%d')