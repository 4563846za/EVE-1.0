import discord
import json
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'

@bot.command(name="character", pass_context=True, aliases=['char'])
async def character(ctx, character_name: str = None):
    user_id = str(ctx.author.id)

    # เปิดไฟล์และตรวจสอบคีย์ 'characters'
    with open("characters.json", "r+") as file:
        data = json.load(file)

        # หากผู้ใช้ไม่มีข้อมูลใน 'characters' ให้สร้างคีย์ให้
        if user_id not in data:
            data[user_id] = {"characters": [], "active_character": None}

        if not data[user_id]["characters"]:
            await ctx.send("คุณยังไม่มีตัวละครที่บันทึกไว้")
            return

        if character_name:
            character = next((char for char in data[user_id]["characters"] if char['name'] == character_name), None)
            if not character:
                await ctx.send(f"ไม่พบตัวละครที่มีชื่อ {character_name}")
                return

            data[user_id]["active_character"] = character_name
            file.seek(0)
            json.dump(data, file, indent=4)

            await ctx.send(f"ตัวละคร {character_name} ถูกตั้งเป็นตัวละครหลักเรียบร้อยแล้ว!")
        else:
            active_name = data[user_id]["active_character"]
            if not active_name:
                await ctx.send("คุณยังไม่ได้เลือกตัวละครหลัก.")
                return

            active_character = next((char for char in data[user_id]["characters"] if char['name'] == active_name), None)
            if active_character:
                await ctx.send(f"ตัวละครหลักที่คุณกำลังใช้คือ: {active_character['name']} ({active_character['race_full_name']} {active_character['background_name']})")
            else:
                await ctx.send("ไม่พบตัวละครหลักที่เลือกไว้")

