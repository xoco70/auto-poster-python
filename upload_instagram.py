from instabot import Bot
import os
from dotenv import load_dotenv
load_dotenv()

INSTA_LOGIN = os.getenv('INSTA_LOGIN')
INSTA_PASS = os.getenv('INSTA_PASS')

bot = Bot()
bot.login(username=INSTA_LOGIN, password=INSTA_PASS)

# file = open('https://catalogue.cappiello.fr/wp-content/uploads/2024/07/43982783c6849ea9f14be41521a84465.jpg', 'r')
# bot.upload_photo(file, caption="Veco, 1934")