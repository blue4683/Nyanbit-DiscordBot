import os
from dotenv import load_dotenv

from nyanbit.core.bot import Nyanbit

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Nyanbit(TOKEN)
bot.start()
