import discord
from discord.ext import commands
from discord import Member
import random
import re   

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())



eve_icon = 'https://media.discordapp.net/attachments/1012033549207076894/1242194388516601980/IMG_0398z.png?ex=664eed6d&is=664d9bed&hm=6a6c42bc54cba0418926c83ff4d3bdc1958a8355cae7655d0d8dad48091b27b2&=&format=webp&quality=lossless&width=701&height=701'
eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'


@bot.command(pass_context=True, aliases=['r'])
async def roll(ctx, dice: str):
    user: Member = None
    if user is None:
        user = ctx.message.author

    try:
        # ใช้ Regular Expression ในการแยกจำนวนเต๋า, หน้าเต๋า และแต้มบวก/ลบ
        match = re.match(r'(\d+)d(\d+)([+-]\d+)?', dice)
        if not match:
            raise ValueError('รูปแบบที่ใช้ไม่ถูกต้อง')

        fdice = int(match.group(1))
        bdice = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        # ตรวจสอบเงื่อนไขขอบเขตของการทอยเต๋า
        if fdice > 0 and bdice > 0:
            rolls = [random.randint(1, bdice) for _ in range(fdice)]
            total = sum(rolls) + modifier
            result = ', '.join(map(str, rolls))
            crit = any(roll == bdice for roll in rolls)  # ตรวจสอบว่ามีการทอยได้ค่าสูงสุดหรือไม่
            crit_text = ' CRIT!!  โห ใหญ่มากๆ โคตรอูมเลย' if crit else ''
            modifier_text = f' {modifier:+}' if modifier != 0 else ''

            # สร้างข้อความผลลัพธ์ตามเงื่อนไข
            if modifier != 0:
                final_result = f'และได้: **{result}{modifier_text}{crit_text} รวมทั้งหมด {total}**'
            else:
                final_result = f'และได้: **{result}{crit_text}**'

            emmbed = discord.Embed(title=f'The Cause Dice', description=f'มีคนทอยเต๋าต้องสาป {bdice} หน้า')
            emmbed.add_field(name=f'{user.display_name} ได้ทำการทอยเต๋าแห่งชะตากรรม {bdice} หน้า', value=final_result)
            emmbed.set_thumbnail(url=user.display_avatar)
            emmbed.set_image(url='https://media4.giphy.com/media/oOBTO2UcSoaBJewZT0/200w.gif?cid=6c09b952aq8mj4ujgfjznfdpv3u2w0o994ylyvswuq2o1iaj&ep=v1_gifs_search&rid=200w.gif&ct=g')
            emmbed.set_author(name=f"Dice Roller!!", icon_url=eve_icon)
            emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)
            await ctx.send(embed=emmbed)
        else:
            await ctx.send('กรุณาระบุจำนวนและหน้าของเต๋าเป็นตัวเลขบวก')

    except Exception as e:
        print(e)
        await ctx.send('รูปแบบที่ใช้ไม่ถูกต้อง กรุณาใช้รูปแบบตามดังนี้: !roll จำนวนเต๋าdหน้าเต๋า[+/-]แต้มที่เพิ่มเข้ามา')