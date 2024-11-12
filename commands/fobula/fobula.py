import discord
import json
from discord.ext import commands

import pandas as pd
import re

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'


# ชื่อไฟล์ JSON
data_file = 'fcharacter.json'

# ฟังก์ชันในการโหลดข้อมูลจาก JSON
def load_data():
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ฟังก์ชันในการบันทึกข้อมูลลง JSON
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)


character_data = {}

def initialize_character(user_id, sheet):
    # ตั้งค่าเริ่มต้นให้กับ character_data ของ user_id
    character_data[user_id] = {
        "name": sheet.iloc[5, 5],
        "image": sheet.iloc[23, 33] if sheet.iloc[23, 33] else "default_image_url.png",
        "fp": int(sheet.iloc[5, 31]),
        "level": int(sheet.iloc[5, 38]),
        "identity": sheet.iloc[6, 5],
        "origin": sheet.iloc[7, 19],
        "ep": int(sheet.iloc[7, 32]),
        "max_hp": int(sheet.iloc[10, 5]),
        "hp": int(sheet.iloc[12, 5]),
        "max_mp": int(sheet.iloc[14, 5]),
        "mp": int(sheet.iloc[14, 9]),
        "max_ip": int(sheet.iloc[16, 5]),
        "ip": int(sheet.iloc[16, 9]),
        "initiative_modifier": int(sheet.iloc[17, 9]),
        "defense": int(sheet.iloc[18, 9]),
        "md": int(sheet.iloc[19, 9]),
        "armor": sheet.iloc[21, 5],
        "mainhand": sheet.iloc[25, 5],
        "dex": sheet.iloc[9, 17],
        "ins": sheet.iloc[10, 17],
        "mig": sheet.iloc[11, 17],
        "wlp": sheet.iloc[12, 17],
        "zenit": sheet.iloc[39, 5]
    }


@bot.command(pass_context=True, aliases=['fimport'])
async def fimport_sheet(ctx, sheet_url: str):
    user_id = str(ctx.author.id)
    data = load_data()

    # แปลง URL ให้เป็นลิงก์ CSV
    csv_url = sheet_url.replace('/edit?usp=sharing', '/export?format=csv')

    # ตรวจสอบว่าผู้ใช้มีข้อมูลอยู่แล้วหรือไม่
    user_data = next((item for item in data if item["user_id"] == user_id), None)

    if user_data:
        # อัปเดตลิงก์ชีต
        user_data["character"] = csv_url  
        await ctx.send(f"{ctx.author.display_name} has updated the Google Sheets URL to: {csv_url}")
    else:
        # เพิ่มข้อมูลใหม่
        new_entry = {
            "user_id": user_id,
            "character": csv_url,
            "name": "sheet.iloc[5, 5]"  # เปลี่ยนเป็นฟังก์ชันหลังจากอ่านชีต
        }
        data.append(new_entry)
        await ctx.send(f"{ctx.author.display_name} has imported the Google Sheets URL: {csv_url}")

    save_data(data)

@bot.command(pass_context=True, aliases=['fchar'])
async def fcharacter(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    # ค้นหาข้อมูลชื่อชีตของผู้ใช้
    user_data = next((item for item in data if item["user_id"] == user_id), None)

    if user_data:
        cheese_name = user_data["name"]
        sheet_url = user_data["character"]
        await ctx.send(f"{ctx.author.display_name}, your cheese is: {cheese_name} and the sheet URL is: {sheet_url}")
    else:
        await ctx.send(f"{ctx.author.display_name}, you haven't imported a sheet yet.")

def get_character_url(user_id):
    data = load_data()  # โหลดข้อมูลจาก JSON
    user_data = next((item for item in data if item["user_id"] == user_id), None)  # ค้นหาข้อมูลของผู้ใช้

    if user_data:
        return user_data.get("character")  # คืนค่าลิงก์ชีต
    else:
        return None  # ถ้าไม่พบข้อมูลของผู้ใช้



@bot.command()
async def fall(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.message.author

    user_id = str(user.id)
    sheet_url = get_character_url(user_id)

    if not sheet_url:
        await ctx.send(f"{user.display_name}, you haven't imported a sheet yet.")
        return

    sheet = pd.read_csv(sheet_url)

    # ตรวจสอบว่ามีข้อมูล character สำหรับ user_id นี้หรือยัง
    if user_id not in character_data:
        initialize_character(user_id, sheet)

    char_info = character_data[user_id]
    embed = discord.Embed(title=char_info["name"], color=0x66FFFF)

    # ดึงข้อมูลจาก dictionary มาแสดง
    embed.add_field(name="ชื่อ", value=char_info["name"], inline=True)
    embed.add_field(name="ตัวตน", value=char_info["identity"], inline=True)
    embed.add_field(name="แหล่งกำเนิด", value=char_info["origin"], inline=True)
    embed.add_field(name="Level", value=char_info["level"], inline=True)
    embed.add_field(name="Fabula Point", value=f'{char_info["fp"]}', inline=True)
    embed.add_field(name="Experience Points", value=f'{char_info["ep"]}', inline=True)
    embed.add_field(name="HP", value=f'{char_info["hp"]}/{char_info["max_hp"]}', inline=True)
    embed.add_field(name="MP", value=f'{char_info["mp"]}/{char_info["max_mp"]}', inline=True)
    embed.add_field(name="Inventory", value=f'{char_info["ip"]}/{char_info["max_ip"]}', inline=True)

    embed.set_thumbnail(url=user.display_avatar)
    embed.set_author(name=user.display_name, icon_url=user.display_avatar)
    embed.set_footer(text=eve_footer, icon_url=eve_iconf)
    embed.set_image(url=char_info["image"])

    await ctx.send(embed=embed)







@bot.command(pass_context=True, aliases=['fg'])
async def fgame(ctx, *, text, user: discord.Member = None):
    if user is None:
        user = ctx.message.author
    
    user_id = str(user.id)
    sheet_url = get_character_url(user_id)
    
    if not sheet_url:
        await ctx.send(f"{user.display_name}, you haven't imported a sheet yet.")
        return
    
    # อ่านข้อมูลจาก CSV
    sheet = pd.read_csv(sheet_url)

    # เรียกฟังก์ชัน initialize_character เพื่อตั้งค่าเริ่มต้นหากยังไม่มีข้อมูล
    if user_id not in character_data:
        initialize_character(user_id, sheet)

    # ดึงข้อมูล character ของผู้ใช้
    char_info = character_data[user_id]

    # ตั้งค่าค่าสูงสุด
    max_hp = char_info["max_hp"]
    max_mp = char_info["max_mp"]
    max_ip = char_info["max_ip"]
    max_fp = 5  # ตามที่กำหนดในโค้ด

    # ตรวจสอบคำสั่งและจับคู่ตามค่า
    changes = {
        'hp': ('hp', max_hp, r'hp\s*([+-]?\d*)'),
        'mp': ('mp', max_mp, r'mp\s*([+-]?\d*)'),
        'ip': ('ip', max_ip, r'ip\s*([+-]?\d*)'),
        'ep': ('ep', None, r'ep\s*([+-]?\d*)'),
        'fp': ('fp', max_fp, r'fp\s*([+-]?\d*)')
    }

    updated_text = ""
    for key, (attr, max_value, pattern) in changes.items():
        match = re.match(pattern, text)
        if match:
            change = match.group(1)
            if change:
                # แปลง change เป็น int ก่อนบวก
                char_info[attr] += int(change)
                if max_value is not None:
                    char_info[attr] = max(0, min(char_info[attr], max_value))
            # อัปเดตค่าใน character_data เสมอ
            updated_text += f"**{key.upper()}**: {int(char_info[attr])}{'/' + str(max_value) if max_value else ''}\n"

    # สร้าง embed และส่งข้อความ
    embed = discord.Embed(title='Character Update', description=updated_text, color=0x66FFFF)
    embed.set_author(name=user.display_name, icon_url=user.display_avatar)
    embed.set_footer(text=eve_footer, icon_url=eve_iconf)
    embed.set_thumbnail(url=char_info["image"])  # ใช้ค่า image ที่กำหนดไว้ใน char_info
    await ctx.send(embed=embed)