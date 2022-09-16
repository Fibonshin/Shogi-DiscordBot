import discord
import cshogi
from discord import Option
import os
from PIL import Image
import glob
TOKEN = "ここにトークンを入力"
bot = discord.Bot()
GUILD_IDS = ["サーバーのIDを入力"]

BOARD=Image.open("img/BOARD.png")
EMPTY=Image.open("img/EMPTY.png")
# 先手駒画像データ komas_S={"GI":<data of GI.png>,"KI":<data of KI.png>,......}
komas_S={os.path.splitext(os.path.basename(name))[0]:Image.open(name) for name in glob.glob("img/koma/*.png")}
#後手駒画像データ
komas_G={os.path.splitext(os.path.basename(name))[0]:Image.open(name).rotate(180) for name in glob.glob("img/koma/*.png")}
num_imgs={os.path.splitext(os.path.basename(name))[0]:Image.open(name) for name in glob.glob("img/num/*.png")}
motigoma_list=["FU","KY","KE","GI","KI","KA","HI"]

async def move_koma(csa):
    global teban
    global pre_motigoma
    bef_x=int(csa[0])
    bef_y=int(csa[1])
    aft_x=int(csa[2])
    aft_y=int(csa[3])
    koma=csa[4:6]
    BOARD.paste(EMPTY,(904-88*bef_x,-61+88*bef_y))
    if teban=="先":
        await moti_koma(0)
        BOARD.paste(komas_S[koma],(904-88*aft_x,-61+88*aft_y))
    else:
        await moti_koma(1)
        BOARD.paste(komas_G[koma],(904-88*aft_x,-61+88*aft_y))
    pre_motigoma=board.pieces_in_hand
    BOARD.save("img/FOR_SEND.png")

async def moti_koma(sengo):
    if sengo==0:koma=komas_S
    else:koma=komas_G
    if board.pieces_in_hand[sengo]!=pre_motigoma[sengo]:
        for i in range(7):
            num_koma=board.pieces_in_hand[sengo][i]
            if num_koma ==0:
                BOARD.paste(EMPTY,(914-900*sengo,203+88*(i-2*i*sengo)+sengo*344))
            if num_koma!=0:
                BOARD.paste(koma[motigoma_list[i]],(914-900*sengo,203+88*(i-2*i*sengo)+sengo*344))
            if 2<=num_koma<=9:
                BOARD.paste(num_imgs[f"number_digtal{num_koma}"],(975-900*sengo,263+88*(i-2*i*sengo)+sengo*352))
            



@bot.event
async def on_ready():
    print("僕は銀ラタウンに住む駆け出しの将棋少年。飛車チューとともにタイトル保持者を倒して、絶対に棋士モンマスターになってやるぜ！(BOT起動しました)")

@bot.slash_command(description="２人で対局できます", guild_ids=GUILD_IDS)
async def taikyoku(
    ctx: discord.ApplicationContext,
):
    global board,teban,pre_motigoma,tesuu,BOARD
    teban = "後"
    tesuu =2
    board = cshogi.Board()
    BOARD=Image.open("img/BOARD.png")
    pre_motigoma=board.pieces_in_hand
    embed = discord.Embed(title="先手番",description="1手目です\n\
\n\
駒名:歩から玉まで:FU,KY,KE,GI,KI,KA,HI,OU、\n\
上の成駒:TO,NY,NK,NG,UM,RY位置:1一を11、\n\
5一を51、9九を99というふうに、2桁の数字で表す。駒台は00とする。\n\
指し手は移動前、移動後の位置、移動後の駒名、で表す。\n\
例:\n\
3324NG=▲2四銀成") 
    await ctx.respond(embed=embed)
    await ctx.send(file=discord.File("img/BOARD.png"))
    BOARD.save("img/FOR_SEND.png")

@bot.slash_command(description="指す！(先に/taikyokuしてね)", guild_ids=GUILD_IDS)
async def sasu(
    ctx: discord.ApplicationContext,
    text: Option(str, required=True, description="指し手", )
):
    global teban,tesuu,board
    if not(text in [cshogi.move_to_csa(move) for move in board.legal_moves]):
        await ctx.respond("その手は無効です")
        return
    move = board.push_csa(text)  
    hoge=teban
    if teban == "後":teban = "先"
    elif teban == "先":teban = "後"
    await move_koma(text)  
    embed = discord.Embed(title=hoge+"手番",description=f"{tesuu}手目です")
    tesuu +=1
    if board.is_game_over():
        embed = discord.Embed(title="詰み",description=f"{teban}手の勝利です！")
    await ctx.respond(embed=embed)
    await ctx.send(file=discord.File("img/FOR_SEND.png"))
    

bot.run(TOKEN)