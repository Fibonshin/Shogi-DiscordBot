import discord
import cshogi
from discord import Option
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = discord.Bot()
GUILD_IDS = [1016139630309015603]
@bot.slash_command(description="２人で対局できます", guild_ids=GUILD_IDS)
async def taikyoku(
    ctx: discord.ApplicationContext,
):
    global board
    global sengo
    sengo = "先"
    board = cshogi.Board()
    await ctx.respond("```横の1～9と縦のa~iを組み合わせ位置を表します。移動前の位置+移動後の位置で駒を動かします(ex.76歩→7g7f)。「成」→  末尾に＋。「打」→歩金銀桂香角飛の順にPGSNLBRのいずれか+*+打つ場所(ex.52銀打→S*5b)```"+"```" + str(board) + "```先手番です")

@bot.slash_command(description="指す！", guild_ids=GUILD_IDS)
async def sasu(
    ctx: discord.ApplicationContext,
    text: Option(str, required=True, description="内容", )
):
    global sengo
    if not(text in [cshogi.move_to_usi(move) for move in board.legal_moves]):
        await ctx.respond("その手は無効です")
        return
    move = board.push_usi(text)    
    if board.is_game_over():
        await ctx.respond("```" + str(board) + "```"+sengo+"手の勝ちです🎉")
        return
    if sengo == "後":sengo = "先"
    elif sengo == "先":sengo = "後"
    await ctx.respond("```" + str(board) + "```"+sengo+"手番です")

    
    

bot.run(TOKEN)