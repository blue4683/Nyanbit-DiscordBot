import db
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pymysql
from typing import Optional

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
APPLICATION_ID = os.getenv("APPLICATION_ID")

description = """
Test bot for myself.
"""

connection = db.Connection()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Bot(
    description=description,
    intents=intents,
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command(name="hello")
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


@bot.command(name="유저추가")
async def add(ctx, member: Optional[discord.Member]):
    try:
        conn, cur = connection.get_connection()

    except:
        print(f"[알림] DB와의 연결에 실패했습니다.")
        await ctx.respond(f"[알림] 현재 DB가 오프라인입니다. 잠시 후에 다시 시도해주십시오.")

    sql = '''
    INSERT INTO userinfo (user_id, user_name) VALUES (%s, %s);
    INSERT INTO nyanbit (user_id, nyanbit_cnt) VALUES (%s, %s);
    '''

    try:
        cur.execute(sql, (member.name, member.display_name, member.name, 0))
        conn.commit()
        conn.close

        await ctx.respond(f"[알림] DB에 {member.display_name}님을 추가했습니다.")

    except pymysql.err.IntegrityError as error:
        print(error)

        await ctx.respond(f"[알림] {member.display_name}님은 DB에 이미 추가된 유저입니다.")


@bot.command(name="지급")
async def give(ctx, name: str, cnt: int):
    conn, cur = connection.get_connection()
    sql = 'SELECT * FROM userinfo WHERE user_name = %s'
    cur.execute(sql, name)
    result = cur.fetchone()

    user_id = result['user_id']
    sql = 'SELECT * FROM nyanbit WHERE user_id = %s'
    cur.execute(sql, user_id)
    result = cur.fetchone()

    print(result)

    await ctx.respond(f"{name}에게 {cnt}개를 지급했습니다.")

bot.run(TOKEN)
