from nyanbit.core.bot import Nyanbit
from .stream import Stream


async def setup(bot: Nyanbit):
    await bot.add_cog(Stream(bot))
