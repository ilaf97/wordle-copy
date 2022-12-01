import schedule
import time
from src.service.wordService import WordService


def select_new_word():
	ws = WordService()
	word = ws.select_word()
	ws.add_word(word)
	return


schedule.every().day.at('00:00').do(select_new_word)

while True:
	schedule.run_pending()
	time.sleep(60)
