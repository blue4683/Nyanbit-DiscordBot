import asyncio
import os

import discord
from discord.ext import commands


class Nyanbit:
    def __init__(self, token):
        self.bot = None
        self.token = token

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
            if ext.endswith(".py"):
                print(f"cogs.{ext.split('.')[0]}")
                await self.bot.load_extension(f"cogs.{ext.split('.')[0]}")
