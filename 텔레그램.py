import telegram
import datetime as dt
 
token = "5648875021:AAEsc8Q86tJhk4hwu2ohLmGQD9gpeYKPRJI"
id = "5669537551"
 
bot = telegram.Bot(token)
bot.sendMessage(chat_id=id, text="테스트 코드")

today = dt.datetime.now().strftime('%Y%m%d')
print(today)