import discord
import cshogi
from discord import Option
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw,ImageFilter
import glob

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = discord.Bot()
# GUILD_IDS = [879288794560471050] honnban
GUILD_IDS = [1016139630309015603] #debug

BOARD=Image.open("img/BOARD.png")
EMPTY=Image.open("img/EMPTY.png")
# 先手駒画像データ komas_S={"GI":<data of GI.png>,"KI":<data of KI.png>,......}
komas_S={os.path.splitext(os.path.basename(name))[0]:Image.open(name) for name in glob.glob("img/koma/*.png")}
#後手駒画像データ
komas_G={os.path.splitext(os.path.basename(name))[0]:Image.open(name).rotate(180) for name in glob.glob("img/koma/*.png")}
teban="先"


async def move_koma(csa):
    global teban
    bef_x=int(csa[0])
    bef_y=int(csa[1])
    aft_x=int(csa[2])
    aft_y=int(csa[3])
    koma=csa[4:6]
    BOARD.paste(EMPTY,(904-88*bef_x,-61+88*bef_y))
    if teban=="先":
        BOARD.paste(komas_S[koma],(904-88*aft_x,-61+88*aft_y))
    else:
        BOARD.paste(komas_G[koma],(904-88*aft_x,-61+88*aft_y))
    BOARD.save("img/FOR_SEND.png")

@bot.event
async def on_ready():
    print("僕は銀ラタウンに住む駆け出しの将棋少年。飛車チューとともにタイトル保持者を倒して、絶対に棋士モンマスターになってやるぜ！(BOT起動しました)")

@bot.slash_command(description="２人で対局できます", guild_ids=GUILD_IDS)
async def taikyoku(
    ctx: discord.ApplicationContext,
):
    global board
    global teban
    teban = "先"
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
    global teban
    if not(text in [cshogi.move_to_csa(move) for move in board.legal_moves]):
        await ctx.respond("その手は無効です")
        return
    move = board.push_csa(text)  
    await move_koma(text)  
    embed = discord.Embed(title=teban+"手番",description="何かいたらいいん") # TODO: 手数出力
    embed.set_image(url="img/FOR_SEND.png") # FIXME: HTTPじゃないと画像を送れない
    await ctx.respond(embed=embed)
    
    if board.is_game_over():
        await ctx.respond("```" + str(board) + "```"+teban+"手の勝ちです🎉")
        return
    if teban == "後":teban = "先"
    elif teban == "先":teban = "後"
    await ctx.respond("```" + str(board) + "```"+teban+"手番です")
    print(board.pieces_in_hand) # TODO :これを用いて持ち駒実装
    

bot.run(TOKEN)