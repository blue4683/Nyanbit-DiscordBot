from nyanbit.core.bot import Nyanbit
from .gamble import Gamble


async def setup(bot: Nyanbit):
    await bot.add_cog(Gamble(bot))
