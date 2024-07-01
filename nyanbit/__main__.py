import db
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import pymysql

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

bot = commands.Bot(
    command_prefix='/',
    description=description,
    intents=intents,
)


def is_allowed():
    async def predicate(ctx):

        try:
            conn, cur = connection.get_connection()

        except:
            print(f"[알림] DB와의 연결에 실패했습니다.")
            await ctx.send(f"[알림] 현재 DB가 오프라인입니다. 잠시 후에 다시 시도해주십시오.")

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


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
@commands.is_owner()  # Prevent other people from using the command
async def sync(ctx: commands.Context) -> None:
    """Sync app commands to Discord."""
    await ctx.bot.tree.sync()
    await ctx.send('Application commands synchronized!')


@bot.hybrid_command(name="관리자등록", description="관리자 권한을 부여합니다. (관리자만 가능)")
@app_commands.describe(
    member='권한을 부여할 유저를 선택해주세요.',
)
@app_commands.rename(
    member='이름',
)
@commands.is_owner()
async def give_admin(ctx, member: discord.Member):
    """
    관리자 권한을 부여합니다. (관리자만 가능)\n
    봇을 제외한 유저를 선택해 관리자 권한을 부여해주세요.

    Parameters
    -----------
    member: discord.Member
    권한을 부여할 유저를 선택해주세요.
    """

    try:
        conn, cur = connection.get_connection()

    except:
        print(f"[알림] DB와의 연결에 실패했습니다.")
        await ctx.send(f"[알림] 현재 DB가 오프라인입니다. 잠시 후에 다시 시도해주십시오.")

    sql = '''
    UPDATE userinfo SET is_admin = 1 WHERE user_id = %s;
    '''

    try:
        cur.execute(sql, member.name)
        conn.commit()
        conn.close()

        await ctx.send(f"[알림] {member.display_name}님에게 관리자 권한을 부여했습니다.")

    except pymysql.err.IntegrityError as error:
        print(error)

        await ctx.send(f"[알림] {member.display_name}님은 관리자입니다.")


@bot.hybrid_command(name="관리자해제", description="관리자 권한을 제거합니다. (관리자만 가능)")
@app_commands.describe(
    member='권한을 제거할 유저를 선택해주세요.',
)
@app_commands.rename(
    member='이름',
)
@commands.is_owner()
async def remove_admin(ctx, member: discord.Member):
    """
    관리자 권한을 제거합니다. (관리자만 가능)\n
    봇을 제외한 유저를 선택해 관리자 권한을 제거해주세요.

    Parameters
    -----------
    member: discord.Member
    권한을 제거할 유저를 선택해주세요.
    """

    try:
        conn, cur = connection.get_connection()

    except:
        print(f"[알림] DB와의 연결에 실패했습니다.")
        await ctx.send(f"[알림] 현재 DB가 오프라인입니다. 잠시 후에 다시 시도해주십시오.")

    sql = '''
    UPDATE userinfo SET is_admin = 0 WHERE user_id = %s;
    '''

    try:
        cur.execute(sql, member.name)
        conn.commit()
        conn.close()

        await ctx.send(f"[알림] {member.display_name}님의 관리자 권한을 제거했습니다.")

    except pymysql.err.IntegrityError as error:
        print(error)

        await ctx.send(f"[알림] {member.display_name}님은 관리자가 아닙니다.")


@bot.hybrid_command(name="유저추가", description="등록되지 않은 유저를 추가합니다.")
@app_commands.describe(
    member='등록할 유저를 선택해주세요.',
)
@app_commands.rename(
    member='이름'
)
@is_allowed()
async def add(ctx, member: discord.Member):
    """
    등록되지 않은 유저를 추가합니다.\n
    봇을 제외한 유저를 선택해 유저를 추가해주세요.

    Parameters
    -----------
    member: discord.Member
    등록할 유저를 선택해주세요.
    """

    try:
        conn, cur = connection.get_connection()

    except:
        print(f"[알림] DB와의 연결에 실패했습니다.")
        await ctx.send(f"[알림] 현재 DB가 오프라인입니다. 잠시 후에 다시 시도해주십시오.")

    sql = '''
    INSERT INTO userinfo (user_id, user_name) VALUES (%s, %s);
    INSERT INTO nyanbit (user_id, nyanbit_cnt) VALUES (%s, %s);
    '''

    try:
        cur.execute(sql, (member.name, member.display_name, member.name, 0))
        conn.commit()
        conn.close

        await ctx.send(f"[알림] DB에 {member.display_name}님을 추가했습니다.")

    except pymysql.err.IntegrityError as error:
        print(error)

        await ctx.send(f"[알림] {member.display_name}님은 DB에 이미 추가된 유저입니다.")


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('관리자 권한이 없는 유저는 사용할 수 없는 명령어 입니다.')


@bot.hybrid_command(name="지급", description="유저에게 nyanbit를 n개 지급합니다.")
@app_commands.describe(
    member='지급할 유저를 선택해주세요.',
    cnt='지급할 개수를 적어주세요. (0이상의 정수만 가능)',
)
@app_commands.rename(
    member='이름',
    cnt='개수'
)
@is_allowed()
async def give(ctx, member: discord.Member, cnt: int):
    """
    등록되지 않은 유저를 추가합니다.\n
    봇을 제외한 유저를 선택해 유저를 추가해주세요.

    Parameters
    -----------
    member: discord.Member
    지급할 유저를 선택해주세요.

    cnt: int
    지급할 개수를 적어주세요. (0이상의 정수만 가능)
    """
    conn, cur = connection.get_connection()
    sql = 'SELECT * FROM nyanbit WHERE user_id = %s'
    cur.execute(sql, member.name)
    result = cur.fetchone()

    if result is None:
        await ctx.send(f"[알림] {member.display_name}은 등록되지 않은 유저입니다. '/유저추가' 명령어를 통해 등록을 먼저 해주세요.")

    sql = 'UPDATE nyanbit SET nyanbit_cnt = %s WHERE user_id = %s'
    cur.execute(sql, (result['nyanbit_cnt'] + cnt, member.name))
    conn.commit()
    conn.close

    await ctx.send(f"[알림] {member.display_name}님에게 {cnt}개를 지급했습니다.")


@give.error
async def give_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('관리자 권한이 없는 유저는 사용할 수 없는 명령어 입니다.')

bot.run(TOKEN)
