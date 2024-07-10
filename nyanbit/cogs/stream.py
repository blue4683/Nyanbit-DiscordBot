import datetime
import os
import pymysql
from dotenv import load_dotenv
from core.db import connection

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()
CHANNEL_ID = os.getenv("CHANNEL_ID")


class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = connection
        self.allow_notification_list = set()

    @commands.Cog.listener("on_voice_state_update")
    async def check_streaming(self, member, before, after):
        if after.self_stream and member.name in self.allow_notification_list:
            channel = self.bot.get_channel(int(CHANNEL_ID))
            await channel.send(f"[알림] {member.display_name}이 방송하고 있습니다.")

    @commands.hybrid_command(name="방송알림허용", description="유저(자신)가 방송을 시작할 때 알림을 보내는 것을 허용합니다.")
    async def allow_notification(self, ctx):
        """
        유저 자신이 방송을 켰을 때의 알림을 허용하는 명령어입니다.
        """
        await self.set_notification(ctx, True)

    @commands.hybrid_command(name="방송알림거부", description="유저(자신)가 방송을 시작할 때 알림을 보내는 것을 거부합니다.")
    async def deny_notification(self, ctx):
        """
        유저 자신이 방송을 켰을 때의 알림이 가지 않도록하는 명령어입니다.
        """
        await self.set_notification(ctx, False)

    async def set_notification(self, ctx, allow: bool):
        conn, cur = self.connection.get_connection()
        user_id = ctx.author.name
        is_allowed_notification = 1 if allow else 0
        action = "허용" if allow else "거부"

        try:
            sql = 'UPDATE userinfo SET is_allowed_notification = %s WHERE user_id = %s;'
            cur.execute(sql, (is_allowed_notification, user_id))
            conn.commit()

            sql = 'SELECT user_id FROM userinfo WHERE is_allowed_notification = 1;'
            cur.execute(sql)
            result = cur.fetchall()

            allow_notification_list = set()
            for res in result:
                allow_notification_list.add(res['user_id'])

            self.allow_notification_list = allow_notification_list
            conn.close()

            await ctx.send(f"[알림] {ctx.author.display_name}님이 방송 알림을 {action}했습니다.")

        except:
            await ctx.send(f"[알림] {ctx.author.display_name}님은 등록되지 않은 유저입니다.")

    @commands.hybrid_command(name="구독알림설정", description="알림을 허용한 유저가 방송을 시작했을 때 알림을 받습니다.")
    @app_commands.describe(
        member='구독해서 알림을 받을 유저를 선택해주세요.',
    )
    @app_commands.rename(
        member='이름',
    )
    async def subscribe(self, ctx, member: discord.Member):
        """
        알림을 허용한 유저가 방송을 시작했을 때 알림을 받습니다.\n
        봇을 제외한 유저를 선택해주세요.

        Parameters
        -----------
        member: discord.Member
        구독할 유저를 선택해주세요.
        """
        conn, cur = self.connection.get_connection()
        check_member = self.is_allowed_notification(cur, member)
        if check_member is None:
            return await ctx.send(f"[알림] {member.display_name}님은 등록되지 않은 유저입니다.")

        if check_member['is_allowed_notification'] == '0':
            return await ctx.send(f"[알림] {member.display_name}님은 방송 알림을 거부한 유저입니다.")

        streamer_id = member.name
        streamer_name = member.display_name
        subscriber_id = ctx.author.name

        try:
            sql = 'INSERT INTO subscriptions (streamer_id, subscriber_id, subscribed_at) VALUES (%s, %s, %s);'
            cur.execute(sql, (streamer_id, subscriber_id, datetime.now()))
            conn.commit()
            conn.close()

            await ctx.send(f"[알림] {ctx.author.display_name}님이 {streamer_name}님을 구독했습니다.")

        except pymysql.err.IntegrityError:
            await ctx.send(f"[알림] {ctx.author.display_name}님은 이미 {streamer_name}님을 구독하고 있습니다.")

    @commands.hybrid_command(name="구독알림해제", description="구독을 취소하여 유저의 방송 알림을 받지 않습니다.")
    @app_commands.describe(
        member='구독을 취소할 유저를 선택해주세요.',
    )
    @app_commands.rename(
        member='이름',
    )
    async def unsubscribe(self, ctx, member: discord.Member):
        """
        구독을 취소하여 유저의 방송 알림을 받지 않습니다.\n
        봇을 제외한 유저를 선택해주세요.

        Parameters
        -----------
        member: discord.Member
        구독을 취소할 유저를 선택해주세요.
        """
        conn, cur = self.connection.get_connection()
        streamer_id = member.name
        streamer_name = member.display_name
        subscriber_id = ctx.author.name

        try:
            sql = 'SELECT EXISTS (SELECT 1 FROM subscriptions WHERE streamer_id = %s AND subscriber_id = %s);'
            cur.execute(sql, (streamer_id, subscriber_id))
            result = cur.fetchone()
            if result[0] == 0:
                return await ctx.send(f"[알림] {ctx.author.display_name}님은 {streamer_name}님을 구독하고 있지 않습니다.")

            sql = 'DELETE FROM subscriptions WHERE streamer_id = %s AND subscriber_id = %s;'
            cur.execute(sql, (streamer_id, subscriber_id))
            conn.commit()
            conn.close()

            await ctx.send(f"[알림] {ctx.author.display_name}님이 {streamer_name}님을 구독 취소했습니다.")

        except pymysql.err.IntegrityError as error:
            print(error)

            await ctx.send(f"[알림] 구독 취소에 실패했습니다.")

    def is_allowed_notification(cur, member: discord.Member):
        sql = 'SELECT is_allowed_notification FROM userinfo WHERE user_id = %s;'
        cur.execute(sql, member.name)
        result = cur.fetchone()

        return result


async def setup(bot):
    await bot.add_cog(Stream(bot))
