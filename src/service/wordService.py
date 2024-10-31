import random
import logging
from typing import Any

from sqlalchemy import func, update
from src.model.wordModel import Word
from src.utils.validations import Validators
from datetime import datetime, timedelta, date
from src import db


class WordService:
    

    def _handle_null_word_object(self, field: str, field_value: Any):
        e = f'Cannot retrieve word from database for {field} with value {str(field_value)}'
        logging.warning(e)
        raise IOError(e)
    
    def _add_word_selected_date(self, id: int) -> None:
        print(f'ID: {id}')
        update_statement = update(Word).where(Word.id==id).values(selected_date=datetime.now().date())
        db.session.execute(update_statement)
        db.session.commit()

    def add_word(self, word: str) -> bool:
        existing_word = Word.query.filter_by(word=word).first()
        if existing_word:
            logging.warning(f"Word '{word}' already exists.")
            return False
    
        word_validation_error = Validators.word(word)
        if word_validation_error != word:
            logging.warning(word_validation_error)
            return False
    
        word_model = Word(word=word)
        db.session.add(word_model)
        db.session.commit()
        logging.info('New word added')
        return True
   

    def get_word(self, date: date | None = None) -> str:
        if date is not None and date < datetime.now().date():
            word_object = Word.query.filter_by(selected_date=date).first()
            if word_object is None:
                self._handle_null_word_object("selected_date", date)
                return
            self._add_word_selected_date(word_object.id)
            return word_object.word
        
        # Assume user retrieving today's word
        todays_word_object = Word.query.filter_by(selected_date=datetime.now().date()).first()
        #print(f'WORD: {todays_word_object.word}')
        if todays_word_object is not None:
            return todays_word_object.word
        
        todays_word_object = self.select_random_word()
        print("INSIDE")
        return todays_word_object.word # type: ignore
        
        
        
    def select_random_word(self) -> Word | None:
        """
        Picks random word from DB that has not been selected for last 3 months.
        Will searhc for 50 entries in DB before failing
        """
        max_id = db.session.query(func.max(Word.id)).scalar()
        i = 0
        while i < 50:
            id_to_select = random.randint(1 , max_id)
            word_object = db.session.query(Word).filter(Word.id==id_to_select).first()
            if word_object is None:
                self._handle_null_word_object("id", id_to_select)
                # Return as this indicates data issue

            three_months_ago: datetime = datetime.now() - timedelta(weeks=13)
            if word_object.selected_date is None or word_object.selected_date < three_months_ago:
                self._add_word_selected_date(word_object.id)
                return word_object
            i += 1
            if i == 50:
                # TODO: make this a custom error
                raise ValueError("Failed to find word older than 3 months")
        