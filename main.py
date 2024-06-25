import db
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
APPLICATION_ID = os.getenv("APPLICATION_ID")

description = """
An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.
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


@bot.command(description="For when you wanna settle the score some other way")
async def choose(ctx: commands.Context, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command(name="hello")
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


@bot.command(name="유저추가")
async def add(ctx, name: str, id: str):
    conn, cur = connection.get_connection()
    sql = 'INSERT INTO userinfo (user_id, user_name) VALUES (%s, %s);'
    cur.execute(sql, (id, name))
    conn.commit()
    conn.close

    await ctx.respond(f"[알림] DB에 {name}을(를) 추가했습니다.")


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
