from core.db import connection

import discord
import typing
from discord import app_commands
from discord.ext import commands


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = connection

    @commands.hybrid_command(name="확인", description="특정 유저 또는 모든 유저의 nyanbit 개수를 확인합니다.")
    @app_commands.describe(
        member='확인할 유저를 선택해주세요. 선택X 시 모든 유저',
    )
    @app_commands.rename(
        member='이름',
    )
    async def check(self, ctx, member: typing.Optional[discord.Member]):
        """
        특정 유저 또는 모든 유저의 nyanbit 개수를 확인합니다.\n
        이름을 선택하면 그 유저의 개수를, 선택하지 않으면 모든 유저의 개수를 확인합니다.

        Parameters
        -----------
        member: typing.Optional[discord.Member]
        확인할 유저를 선택해주세요. (선택하지 않을 시 모든 유저)
        """
        conn, cur = self.connection.get_connection()
        if member:
            try:
                sql = 'SELECT user_name, nyanbit FROM userinfo WHERE user_id = %s'
                cur.execute(sql, member.id)
                result = cur.fetchone()

                await ctx.send(f"[알림] {result['user_name']}님은 {result['nyanbit']}개를 가지고 있습니다.")

            except:
                await ctx.send(f"[알림] {member.display_name}님은 없는 유저입니다.")

        else:
            sql = 'SELECT user_name, nyanbit FROM userinfo'
            cur.execute(sql)
            result = cur.fetchall()

            txt = ''
            for res in result:
                txt += f"{res['user_name']} - {res['nyanbit']}개\n"

            if not txt:
                await ctx.send(f"[알림] 현재 등록된 유저가 없습니다. '/유저추가' 명령어를 통해 유저를 등록해주세요.")

            else:
                await ctx.send(f"[알림]\n{txt}")

    @commands.hybrid_command(name="상환", description="유저에게 빌린 nyanbit n개를 상환합니다.")
    @app_commands.describe(
        member='상환할 유저를 선택해주세요.',
        cnt='상환할 개수를 적어주세요. (0이상의 정수만 가능)',
    )
    @app_commands.rename(
        member='이름',
        cnt='개수'
    )
    async def pay_back(self, ctx, member: discord.Member, cnt: int):
        """
        유저에게 nyanbit n개를 상환합니다.\n
        봇을 제외한 유저를 선택해주세요.

        Parameters
        -----------
        member: discord.Member
        상환할 유저를 선택해주세요.

        cnt: int
        상환할 개수를 적어주세요. (0이상의 정수만 가능)
        """
        conn, cur = self.connection.get_connection()

        sql = 'SELECT nyanbit FROM userinfo WHERE user_id = %s'
        cur.execute(sql, ctx.author.id)
        owner = cur.fetchone()

        if owner is None:
            return await ctx.send(f"[알림] {ctx.author.display_name}님은 등록되지 않은 유저입니다. '/유저추가' 명령어를 통해 등록을 먼저 해주세요.")

        if owner['nyanbit'] < cnt:
            return await ctx.send(f"[알림] {ctx.author.display_name}님은 현재 {owner['nyanbit']}를 가지고 있어 {cnt}개를 상환할 수 없습니다.")

        sql = 'SELECT nyanbit FROM userinfo WHERE user_id = %s'
        cur.execute(sql, member.id)
        deptor = cur.fetchone()

        if deptor is None:
            return await ctx.send(f"[알림] {member.display_name}님은 등록되지 않은 유저입니다. '/유저추가' 명령어를 통해 등록을 먼저 해주세요.")

        sql = '''
        UPDATE userinfo SET nyanbit = %s WHERE user_id = %s;
        UPDATE userinfo SET nyanbit = %s WHERE user_id = %s;
        '''
        cur.execute(sql, (owner['nyanbit'] - cnt, ctx.author.id,
                    deptor['nyanbit'] + cnt, member.id))
        conn.commit()
        conn.close

        await ctx.send(f"[알림] {ctx.author.display_name}님이 {member.display_name}님에게 {cnt}개를 상환했습니다.")


async def setup(bot):
    await bot.add_cog(Gamble(bot))
