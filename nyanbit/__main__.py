import os
from dotenv import load_dotenv

from nyanbit.core.bot import Nyanbit
from nyanbit.logging import Logger

load_dotenv()
TOKEN = os.getenv("TOKEN")

Logger._Logger.info("Nyanbit 봇을 실행시킵니다.")
bot = Nyanbit(TOKEN)
bot.start()
