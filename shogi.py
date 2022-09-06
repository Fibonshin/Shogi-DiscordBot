import discord
import cshogi
from discord import Option
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = discord.Bot()
GUILD_IDS = [879288794560471050]

@bot.event
async def on_ready():
    print("僕は銀ラタウンに住む駆け出しの将棋少年。飛車チューとともにタイトル保持者を倒して、絶対に棋士モンマスターになってやるぜ！(BOT起動しました)")

@bot.slash_command(description="２人で対局できます", guild_ids=GUILD_IDS)
async def taikyoku(
    ctx: discord.ApplicationContext,
):
    global board
    global sengo
    sengo = "先"
    board = cshogi.Board()
    await ctx.respond("```駒名:歩から玉まで:FU,KY,KE,GI,KI,KA,HI,OU、\n\
上の成駒:TO,NY,NK,NG,UM,RY位置:1一を11、\n\
5一を51、9九を99というふうに、2桁の数字で表す。駒台は00とする。\n\
指し手は移動前、移動後の位置、移動後の駒名、で表す。\n\
例:\n\
3324NG=▲2四銀成```"+"```" + str(board) + "```先手番です")

@bot.slash_command(description="指す！(先に/taikyokuしてね)", guild_ids=GUILD_IDS)
async def sasu(
    ctx: discord.ApplicationContext,
    text: Option(str, required=True, description="指し手", )
):
    global sengo
    if not(text in [cshogi.move_to_csa(move) for move in board.legal_moves]):
        await ctx.respond("その手は無効です")
        return
    move = board.push_csa(text)    
    if board.is_game_over():
        await ctx.respond("```" + str(board) + "```"+sengo+"手の勝ちです🎉")
        return
    if sengo == "後":sengo = "先"
    elif sengo == "先":sengo = "後"
    await ctx.respond("```" + str(board) + "```"+sengo+"手番です")

    
    

bot.run(TOKEN)