import discord
import json
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'

@bot.command(name="character_list", pass_context=True, aliases=['charlist'])
async def character_list(ctx):
    user_id = str(ctx.author.id)

    # เปิดไฟล์และตรวจสอบคีย์ 'characters'
    with open("characters.json", "r") as file:
        data = json.load(file)

        # หากผู้ใช้ไม่มีข้อมูลใน 'characters' ให้สร้างคีย์ให้
        if user_id not in data:
            data[user_id] = {"characters": [], "active_character": None}

        if not data[user_id]["characters"]:
            await ctx.send("คุณยังไม่มีตัวละครที่บันทึกไว้")
            return

        characters = [char['name'] for char in data[user_id]["characters"]]
        character_list = "\n".join(characters)
        await ctx.send(f"ตัวละครทั้งหมดของคุณ:\n{character_list}")


