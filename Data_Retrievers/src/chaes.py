import telegram
import asyncio

API_TOKEN="6446041095:AAEc1cdBdZToofrWVzelLhWMroksdm5O_Tc"
bot = telegram.Bot(token=API_TOKEN)


chat_id = 1056233292
asyncio.run(bot.send_message(chat_id=-1056233292, text="I Love You"))
