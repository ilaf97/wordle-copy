import random
import logging
from data import word_list
from src.model.wordModel import Word
from src.utils.validations import Validators
from datetime import datetime
from src import db


class WordService:

    def __init__(self):
        self.word_list = word_list
        self.word_count = self._count_input_lines() - 1  # Initial length of word list

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
        if date == '':
            date = self.get_current_date_str()
        word = Word.query.filter_by(date=Word.date.contains(date)).first()
        if word is None:
             e = f'Cannot retrieve word from database for date {date}'
             logging.warning(e)
             raise IOError(e)
        return word.word
        
    def select_word(self) -> str:
        # This would not be a robust long-term method – improve for demo of architecture understanding
        random_num = random.randint(0, self.word_count)
        try:
            with open(self.word_list) as f:
                for index, line in enumerate(f, start=0):
                    if index == random_num:
                        word = line.rstrip()
        except Exception as e:
            logging.fatal('Could not open word_list.txt file')
            logging.fatal(e)
            word = ''
        return word

    @staticmethod
    def get_current_date_str() -> str:
        curr_date = datetime.now()
        return datetime.strftime(curr_date, '%Y-%m-%d')

    def _count_input_lines(self) -> int:
        try:
            with open(self.word_list) as f:
                count = 0
                for line in enumerate(f):
                    count += 1
                if count == 0:
                    raise FileExistsError('No words in word_list.txt')
        except FileExistsError as e:
            logging.fatal(e)
        except Exception as e:
            logging.fatal('Could not open word_list.txt file')
            logging.fatal(e)
        return count

    def _open_word_list_file(self) -> list[str]: # type: ignore
        try:
            with open(self.word_list, 'r') as f:
                return f.readlines()
        except Exception as e:
            logging.warning('Could not open word_list.txt file')
            logging.warning(e)

    def _delete_word_from_list(self, word_to_delete: str) -> None:
        # This seems like a strange way of doing things
        try:
            with open(self.word_list, 'w') as f:
                for line in self._open_word_list_file():
                    if line.strip('\n') != word_to_delete:
                        f.write(line)
                    else:
                        logging.info('Word deleted')
                        self.word_count -= 1
        except Exception as e:
            logging.warning('Could not open word_list.txt file')
            logging.warning(e)
