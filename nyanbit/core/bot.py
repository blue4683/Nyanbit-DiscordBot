import asyncio
import os

import discord
from discord.ext import commands
from nyanbit.logging import Logger


class Nyanbit:
    def __init__(self, token):
        self.bot = None
        self.token = token

    def __del__(self):
        Logger._Logger.info("Nyanbit가 종료됩니다.")

    def start(self):
        asyncio.run(self.initialize())
        self.bot.run(self.token)

    async def initialize(self):
        await self.initialize_bot()
        await self.add_cogs()

    async def initialize_bot(self):
        description = """
        Test bot for myself.
        """

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        self.bot = commands.Bot(
            command_prefix='/',
            description=description,
            intents=intents,
        )

    async def add_cogs(self):
        cogs_path = 'cogs'
        abs_cogs_path = os.path.join(os.path.dirname(
            os.path.abspath(os.path.dirname(__file__))), cogs_path)

        for ext in os.listdir(abs_cogs_path):
            if not ext.startswith("__"):
                await self.bot.load_extension(f"nyanbit.cogs.{ext}")
