from nyanbit.core.bot import Nyanbit
from .admin import Admin


async def setup(bot: Nyanbit):
    await bot.add_cog(Admin(bot))
