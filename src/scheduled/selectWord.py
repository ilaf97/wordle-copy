from src.service.wordService import WordService


def select_new_word(app):
	ws = WordService(app)
	word = ws.select_word()
	ws.add_word(word)
	return word


# schedule.every().day.at('00:00').do(select_new_word)

# while True:
# 	schedule.run_pending()
# 	time.sleep(60)
