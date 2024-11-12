import discord
from discord.ext import commands
import random
import json
import os

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_icons = 'https://media.discordapp.net/attachments/1012033549207076894/1242894958814433370/IMG_0500.png?ex=664f7fa2&is=664e2e22&hm=22b48fa5edd5a831350d04aedb12758cd3b316311982f1cfe3ebb6cdddedaa94&=&format=webp&quality=lossless&width=377&height=350'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'

def load_tarot_cards():
    try:
        with open('tarot_cards.json', encoding='utf-8') as f:
            tarot_cards = json.load(f)
        return tarot_cards
    except FileNotFoundError:
        print("File 'tarot_cards.json' not found")
        return []
    except json.JSONDecodeError:
        print("File 'tarot_cards.json' is not properly formatted")
        return []


# ใช้ path ที่เป็น relative path
BASE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "Tarot")

@bot.command(pass_context=True, aliases=['t', 'tar', 'taro'])
async def tarot(ctx, user: discord.Member=None):
    tarot_cards = load_tarot_cards()
    if tarot_cards:
        card = random.choice(tarot_cards)
        
        # ดึงโฟลเดอร์และชื่อไฟล์ของภาพจาก JSON และรวมกับ BASE_IMAGE_PATH
        folder = card["folder"]
        image = card["image"]
        image_path = os.path.join(BASE_IMAGE_PATH, folder, image)  # ใช้ relative path 

        if user is None:
            user = ctx.message.author

        inline = False
        embed = discord.Embed(
            title=card['name'],
            description=card['description'],
            color=0x00ff00
        )

        simple = {
            '**ความหมาย**': '',
            'ความหมายในเชิงความรัก': card['m1'],
            'หน้าที่การงาน': card['m2'],
            'เรื่องการเงิน': card['m3'],
            'เรื่องการเดินทาง': card['m4'],
            'เรื่องสุขภาพ': card['m5'],
            'ความหมายในเชิงแนะนำ': card['m6']
        }

        for field_name, field_val in simple.items():
            embed.add_field(name=field_name, value=field_val, inline=inline)

        embed.set_author(name="แม่หมอ อีฟ", icon_url=eve_icons)
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(text=eve_footer, icon_url=eve_iconf)

        # ตรวจสอบว่ารูปภาพมีอยู่จริงก่อนส่ง
        if os.path.isfile(image_path):
            with open(image_path, "rb") as img:
                file = discord.File(img, filename=image)
                embed.set_image(url=f"attachment://{image}")
                await ctx.send(embed=embed, file=file)
        else:
            await ctx.send("ไม่พบรูปภาพของไพ่ที่ระบุ")
    else:
        await ctx.send("Tarot card data is not available. Please check 'tarot_cards.json'.")