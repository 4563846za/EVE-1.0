import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# โหลดค่า .env
load_dotenv()

# ดึง token จาก .env
TOKEN = os.getenv("TOKEN")

from commands.tarrot import tarot
from commands.gtts import eveen, eveth, translate, translate_JP
from music import play, play_next, pause, skip, stop, queue, clear_q
from commands.blackjack import blackjack, hit, stand
from commands.voice_chanel import eve, leave

from commands.dnd.roll import roll

from commands.fobula.fobula import fimport_sheet, fcharacter, fall, fgame

from commands.dnd.show_all_character_info import show_all_character_info
from commands.dnd.character_list import character_list
from commands.dnd.character import character
from commands.dnd.import_character import import_character

# สร้างบอท
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# ข้อมูลบอท
eve_icon = 'https://media.discordapp.net/attachments/1012033549207076894/1242194388516601980/IMG_0398z.png?ex=664eed6d&is=664d9bed&hm=6a6c42bc54cba0418926c83ff4d3bdc1958a8355cae7655d0d8dad48091b27b2&=&format=webp&quality=lossless&width=701&height=701'
eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_image = 'https://media.discordapp.net/attachments/1012033549207076894/1237744870500728852/IMG_0397.png?ex=6645fdbd&is=6644ac3d&hm=6500a9bc2947e3764140481bc9f5d851421ac87f7ed3936af7de752376aedb2d&=&format=webp&quality=lossless&width=1079&height=701'
eve_images = 'https://media.discordapp.net/attachments/1012033549207076894/1242894958814433370/IMG_0500.png?ex=664f7fa2&is=664e2e22&hm=22b48fa5edd5a831350d04aedb12758cd3b316311982f1cfe3ebb6cdddedaa94&=&format=webp&quality=lossless&width=377&height=350'
eve_icons = 'https://media.discordapp.net/attachments/1012033549207076894/1242894958814433370/IMG_0500.png?ex=664f7fa2&is=664e2e22&hm=22b48fa5edd5a831350d04aedb12758cd3b316311982f1cfe3ebb6cdddedaa94&=&format=webp&quality=lossless&width=377&height=350'
eve_footer = 'EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'

@bot.event
async def on_ready():
    bgc = bot.get_channel
    eve = 1243548886207827989
    eda = 1154363890713505842
    yokai = 1241064234989780993
    online = [bgc(eve)]
    text = f"EVE ตื่นแล้ว"
    emmbed = discord.Embed(title=text, color=0x66FFFF)

    emmbed.set_image(url=eve_images)
    emmbed.set_author(name="EVE", icon_url=eve_icon)
    emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)

    for on in online:
        await on.send(embed=emmbed)

    await bot.change_presence(status=discord.Status, activity=discord.Activity(type=discord.ActivityType.watching, name="พวกมักมากในกามอยู่"))
    print('EVE ตื่นแล้ว')

# เพิ่มเติมคำสั่งต่าง ๆ เช่น add_command(play), add_command(eveth) ตามโค้ดของคุณ

# เริ่มต้นการทำงานของบอท
bot.run(TOKEN)
