from core.db import connection

import discord
import pymysql
from discord import app_commands
from discord.ext import commands


def is_allowed():
    async def predicate(ctx):
        conn, cur = connection.get_connection()

        sql = '''
        SELECT user_id FROM userinfo WHERE is_admin = 1;
        '''

        cur.execute(sql)
        result = cur.fetchall()
        conn.close()

        for user in result:
            if user['user_id'] == ctx.author.name:
                return 1

        return 0

    return commands.check(predicate)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = connection

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        """Sync app commands to Discord."""
        await ctx.bot.tree.sync()
        await ctx.send('Application commands synchronized!')

    @commands.hybrid_command(name="관리자등록", description="관리자 권한을 부여합니다. (관리자만 가능)")
    @app_commands.describe(
        member='권한을 부여할 유저를 선택해주세요.',
    )
    @app_commands.rename(
        member='이름',
    )
    @commands.is_owner()
    async def give_admin(self, ctx, member: discord.Member):
        await self.set_admin(ctx, member, True)

    @commands.hybrid_command(name="관리자해제", description="관리자 권한을 제거합니다. (관리자만 가능)")
    @app_commands.describe(
        member='권한을 제거할 유저를 선택해주세요.',
    )
    @app_commands.rename(
        member='이름',
    )
    @commands.is_owner()
    async def remove_admin(self, ctx, member: discord.Member):
        await self.set_admin(ctx, member, False)

    async def set_admin(self, ctx, member: discord.Member, is_admin: bool):
        conn, cur = self.connection.get_connection()
        admin_status = 1 if is_admin else 0
        action = "부여" if is_admin else "제거"

        sql = '''
        UPDATE userinfo SET is_admin = %s WHERE user_id = %s;
        '''

        try:
            cur.execute(sql, (admin_status, member.id))
            conn.commit()
            conn.close()

            await ctx.send(f"[알림] {member.display_name}님에게 관리자 권한을 {action}했습니다.")

        except pymysql.err.IntegrityError as error:
            print(error)

            await ctx.send(f"[알림] {member.display_name}님은 등록되지 않은 유저입니다.")

    @commands.hybrid_command(name="유저추가", description="등록되지 않은 유저를 추가합니다.")
    @app_commands.describe(
        member='등록할 유저를 선택해주세요.',
    )
    @app_commands.rename(
        member='이름'
    )
    @is_allowed()
    async def add(self, ctx, member: discord.Member):
        """
        등록되지 않은 유저를 추가합니다.\n
        봇을 제외한 유저를 선택해 유저를 추가해주세요.

        Parameters
        -----------
        member: discord.Member
        등록할 유저를 선택해주세요.
        """

        conn, cur = self.connection.get_connection()

        sql = '''
        INSERT INTO userinfo (user_id, user_name, is_admin, nyanbit) VALUES (%s, %s, %s, %s);
        '''

        try:
            cur.execute(sql, (member.name, member.display_name, 0, 0))
            conn.commit()
            conn.close

            return await ctx.send(f"[알림] DB에 {member.display_name}님을 추가했습니다.")

        except pymysql.err.IntegrityError as error:
            print(error)

            return await ctx.send(f"[알림] {member.display_name}님은 DB에 이미 추가된 유저입니다.")

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('관리자 권한이 없는 유저는 사용할 수 없는 명령어 입니다.')

    @commands.hybrid_command(name="지급", description="유저에게 nyanbit를 n개 지급합니다.")
    @app_commands.describe(
        member='지급할 유저를 선택해주세요.',
        cnt='지급할 개수를 적어주세요. (0이상의 정수만 가능)',
    )
    @app_commands.rename(
        member='이름',
        cnt='개수'
    )
    @is_allowed()
    async def give(self, ctx, member: discord.Member, cnt: int):
        """
        유저에게 nyanbit를 n개 지급합니다.\n
        봇을 제외한 유저를 선택해주세요.

        Parameters
        -----------
        member: discord.Member
        지급할 유저를 선택해주세요.

        cnt: int
        지급할 개수를 적어주세요. (0이상의 정수만 가능)
        """
        conn, cur = self.connection.get_connection()
        sql = 'SELECT nyanbit FROM userinfo WHERE user_id = %s'
        cur.execute(sql, member.name)
        result = cur.fetchone()

        if result is None:
            return await ctx.send(f"[알림] {member.display_name}님은 등록되지 않은 유저입니다. '/유저추가' 명령어를 통해 등록을 먼저 해주세요.")

        sql = 'UPDATE userinfo SET nyanbit = %s WHERE user_id = %s'
        cur.execute(sql, (result['nyanbit'] + cnt, member.name))
        conn.commit()
        conn.close

        return await ctx.send(f"[알림] {member.display_name}님에게 {cnt}개를 지급했습니다.")

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('관리자 권한이 없는 유저는 사용할 수 없는 명령어 입니다.')


async def setup(bot):
    await bot.add_cog(Admin(bot))
