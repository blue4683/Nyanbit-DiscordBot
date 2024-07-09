import os
from dotenv import load_dotenv
from core.db import connection

import discord
from discord import app_commands
from discord.ext import commands

CHANNEL_ID = os.getenv("CHANNEL_ID")


class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = connection

    @commands.Cog.listener("on_voice_state_update")
    async def check_streaming(self, member, before, after):
        if after.self_stream:
            channel = self.bot.get_channel(int(CHANNEL_ID))
            await channel.send(f"[알림] {member.display_name}이 방송하고 있습니다.")


async def setup(bot):
    await bot.add_cog(Stream(bot))
