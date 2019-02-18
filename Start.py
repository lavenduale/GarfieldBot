import os

from dotenv import load_dotenv

from GarfieldBot import Bot

load_dotenv()
bot = Bot(os.environ["GARFIELDBOT_SLACK_TOKEN"])
bot.start()