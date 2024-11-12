import discord
import json
from discord.ext import commands
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'


@bot.command(name="all")
async def show_all_character_info(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.message.author

    user_id = str(ctx.author.id)

    # โหลดข้อมูลจากไฟล์ characters.json
    try:
        with open("characters.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        await ctx.send("ยังไม่มีข้อมูลตัวละครในระบบ")
        return

    # ตรวจสอบว่าผู้ใช้มีข้อมูลตัวละครในไฟล์หรือไม่
    if user_id not in data or not data[user_id]["characters"]:
        await ctx.send("คุณยังไม่มีตัวละครที่บันทึกไว้")
        return

    # ตรวจสอบว่าผู้ใช้มีตัวละครหลักที่ตั้งไว้หรือไม่
    active_name = data[user_id].get("active_character")
    if not active_name:
        await ctx.send("คุณยังไม่ได้เลือกตัวละครหลัก")
        return

    # ค้นหาตัวละครหลักจากชื่อ
    active_character = next((char for char in data[user_id]["characters"] if char['name'] == active_name), None)
    if not active_character:
        await ctx.send("ไม่พบตัวละครหลักที่เลือกไว้")
        return

    # สร้าง Embed สำหรับข้อมูลตัวละคร
    embed = discord.Embed(
        title=f"ข้อมูลเบื้องต้นของ: {active_character.get('name', 'N/A')}",
        color=discord.Color.blue()
    )
    
    # เพิ่มฟิลด์ข้อมูลต่างๆ
    embed.add_field(name="เลเวล", value=active_character.get("level", "ไม่ทราบแน่ชัด"), inline=True)
    embed.add_field(name="เผ่า", value=active_character.get("race_full_name", "ไม่ทราบแน่ชัด"), inline=True)
    embed.add_field(name="อาชีพ", value=active_character.get("class", "ไม่ทราบแน่ชัด"), inline=True)
    embed.add_field(name="เพศ", value=active_character.get("gender", "ไม่ทราบแน่ชัด"), inline=True)
    embed.add_field(name="อายุ", value=active_character.get("age", "ไม่ทราบแน่ชัด"), inline=True)
    embed.add_field(name="HP", value=f"{active_character.get('base_hit_points', 'ไม่ทราบแน่ชัด')} / {active_character.get('base_hit_points', 'ไม่ทราบแน่ชัด')}", inline=True)
    embed.add_field(name="AC", value=active_character.get("armor_class", "ไม่ทราบแน่ชัด"), inline=True)
    
    # แสดงค่า stats (ค่าสเตตัสทั้งหมด)
    stats = active_character.get("stats", {})
    stats_text = "\n".join([f"{stat_name}: {stat_value}" for stat_name, stat_value in stats.items()]) if stats else "ไม่ทราบแน่ชัด"
    embed.add_field(name="ค่าสเตตัส", value=stats_text, inline=False)

    # ตั้งค่ารูปภาพหลักและ thumbnail
    embed.set_thumbnail(url=active_character.get("small_backdrop_avatar_url", ""))
    embed.set_image(url=active_character.get("avatar_url", ""))

    embed.set_footer(text=eve_footer, icon_url=eve_iconf)
    embed.set_author(name=user.display_name, icon_url=user.display_avatar)


    # ส่ง Embed
    await ctx.send(embed=embed)