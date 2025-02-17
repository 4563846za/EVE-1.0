import discord
from discord.ext import commands
from commands.tarrot import tarot
from commands.gtts import eveen, eveth, translate, translate_JP

from commands.blackjack import blackjack, hit, stand
from commands.voice_chanel import eve, leave

from commands.dnd.roll import roll

from commands.fobula.fobula import fimport_sheet, fcharacter, fall, fgame

from commands.dnd.show_all_character_info import show_all_character_info
from commands.dnd.character_list import character_list
from commands.dnd.character import character
from commands.dnd.import_character import import_character

from dotenv import load_dotenv
import os
from myserver import server_on

load_dotenv()


# ดึง token จาก .env
TOKEN = os.getenv("TOKEN")

# สร้างบอท
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())




eve_icon = 'https://media.discordapp.net/attachments/1012033549207076894/1242194388516601980/IMG_0398z.png?ex=664eed6d&is=664d9bed&hm=6a6c42bc54cba0418926c83ff4d3bdc1958a8355cae7655d0d8dad48091b27b2&=&format=webp&quality=lossless&width=701&height=701'
eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_image = 'https://media.discordapp.net/attachments/1012033549207076894/1237744870500728852/IMG_0397.png?ex=6645fdbd&is=6644ac3d&hm=6500a9bc2947e3764140481bc9f5d851421ac87f7ed3936af7de752376aedb2d&=&format=webp&quality=lossless&width=1079&height=701'
eve_images = 'https://media.discordapp.net/attachments/1012033549207076894/1242894958814433370/IMG_0500.png?ex=664f7fa2&is=664e2e22&hm=22b48fa5edd5a831350d04aedb12758cd3b316311982f1cfe3ebb6cdddedaa94&=&format=webp&quality=lossless&width=377&height=350'
eve_icons = 'https://media.discordapp.net/attachments/1012033549207076894/1242894958814433370/IMG_0500.png?ex=664f7fa2&is=664e2e22&hm=22b48fa5edd5a831350d04aedb12758cd3b316311982f1cfe3ebb6cdddedaa94&=&format=webp&quality=lossless&width=377&height=350'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'






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
    emmbed.set_author(name=f"EVE", icon_url=eve_icon)
    emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)

    for on in online:
        await on.send(embed=emmbed)

    await bot.change_presence(status=discord.Status,activity=discord.Activity(type=discord.ActivityType.watching,name="พวกมักมากในกามอยู่"))
    print('EVE ตื่นแล้ว')


@bot.event
async def on_member_join(member):
    ch = bot.get_channel 
    eve = 1243545770679074838
    holi = 1219232051895734326
    welcome = [ch(eve)]
    
    emmbed = discord.Embed(title='Hello Welcome! have room have condom',
                           description=f"ยินดีต้อนรับนะเจ้าบ้ากาม {member.mention}",
                           color=0x66FFFF,
                           timestamp=discord.utils.utcnow())

    emmbed.set_thumbnail(url=member.display_avatar)
    emmbed.set_image(url=eve_image)
    emmbed.set_author(name=f"EVE", icon_url=eve_icon)
    emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)
    
    for wc in welcome:
        await wc.send(embed=emmbed)



@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1243548886207827989)
    emmbed = discord.Embed(title=f"คนเงิ่ยนไปหายไปคนนึงแล้วล่ะ คราวนี้ที่นี่ก็น่าอยู่ขึ้นอีกนิด",
                          color=0x66FFFF,
                          timestamp=discord.utils.utcnow())

    emmbed.set_thumbnail(url=member.display_avatar)
    emmbed.set_image(url=eve_image)
    emmbed.set_author(name=f"EVE", icon_url=eve_icon)
    emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)
    await channel.send(embed=emmbed)


#////////////////////////////////////////////////////////////////////////////////////////////////// MUSIC //////////////////////////////////////////////////////////////////////////////////////////////////

from discord import Member
from discord.utils import get
import urllib.parse, urllib.request, re
import yt_dlp
import asyncio

queues = {}
voice_clients = {}
youtube_base_url = 'https://www.youtube.com/'
youtube_results_url = youtube_base_url + 'results?'
youtube_watch_url = youtube_base_url + 'watch?v='
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}

@bot.event
async def play_next(ctx):
    if queues[ctx.guild.id] != []:
        url = queues[ctx.guild.id].pop(0)
        await play(ctx, url=url)


def format_duration(duration_seconds):
    minutes, seconds = divmod(duration_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"
    
    
@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, *, url, user: Member=None):
    try:
        voice_client = await ctx.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except Exception as e:
        print(e)

    try:

        if youtube_base_url not in url:
            query_string = urllib.parse.urlencode({
                'search_query': url
            })

            content = urllib.request.urlopen(
                youtube_results_url + query_string
            )

            search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

            url = youtube_watch_url + search_results[0]

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        song = data['url']
        player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

        voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx),
                                                                                                  bot.loop))

        if user is None:
            user = ctx.message.author

        inline = False
        ydl = yt_dlp.YoutubeDL()
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'Unknown Title')
        im = info.get('thumbnail', '')
        duration = info.get('duration', 0)
        emmbed = discord.Embed(title=f'{title} ',description='เปิดเพลงให้แล้วน้าา'f' {user.mention}', color=0x66FFFF)
        userData = {
            'Duration':f'{format_duration(duration)}',
            'Link': url,
                    }
        for [fieldName, fieldVal] in userData.items():
            emmbed.set_author(name=f"เปิดเพลงแล้ว", icon_url=eve_icons)
            emmbed.add_field(name=fieldName, value=fieldVal, inline=inline)
        emmbed.set_thumbnail(url=user.display_avatar)
        emmbed.set_image(url=im)
        emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)
        await ctx.send(embed=emmbed)

    except Exception as e:
        print(e)



@bot.command(pass_context=True, aliases=['cl'])
async def clear_q(ctx):
    if ctx.guild.id in queues:
        queues[ctx.guild.id].clear()
        await ctx.send("เคลียเพลงในคิวหมดแล้วน้าาา")
    else:
        await ctx.send("ไม่มีเพลงในคิวนะ จะให้เคลียอะไรอะ")

@bot.command(pass_context=True, aliases=['pa'])
async def pause(ctx):
    try:
        voice_clients[ctx.guild.id].pause()
    except Exception as e:
        print(e)

@bot.command(pass_context=True, aliases=['re'])
async def resume(ctx):
    try:
        voice_clients[ctx.guild.id].resume()
    except Exception as e:
        print(e)

@bot.command(name="stop")
async def stop(ctx):
    try:
        voice_clients[ctx.guild.id].stop()
        await voice_clients[ctx.guild.id].disconnect()
        del voice_clients[ctx.guild.id]
    except Exception as e:
        print(e)

@bot.command(pass_context=True, aliases=['q'])
async def queue(ctx, *, url, user: Member=None):
    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = []
    queues[ctx.guild.id].append(url)
    if user is None:
        user = ctx.message.author

    inline = True
    emmbed = discord.Embed(description='เพิ่มเพลงเข้าคิวให้ละ'f' {user.mention}', color=0x66FFFF)
    userData = {
    }
    for [fieldName, fieldVal] in userData.items():
        emmbed.add_field(name=fieldName, value=fieldVal, inline=inline)
    emmbed.set_author(name=f"คิวเพลงแล้ว", icon_url=eve_icons)

    emmbed.set_thumbnail(url=user.display_avatar)
    emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)

    await ctx.send(embed=emmbed)


@bot.command(pass_context=True, aliases=['s'])
async def skip(ctx, user: Member=None):
    voice_clients = get(bot.voice_clients, guild=ctx.guild)
    if user is None:
        user = ctx.message.author

    inline = True
    emmbed = discord.Embed(description='ข้ามเพลงให้แล้วน้าา'f' {user.mention}', color=0x66FFFF)
    userData = {
    }
    for [fieldName, fieldVal] in userData.items():
                emmbed.add_field(name=fieldName, value=fieldVal, inline=inline)
    emmbed.set_author(name=f"ข้ามเพลงแล้ว", icon_url=eve_icons)
    emmbed.set_thumbnail(url=user.display_avatar)
    emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)

    await ctx.send(embed=emmbed)
    voice_clients.stop()

#///////////////////////////////////////////////////// GTTS /////////////////////////////////////////////////////

bot.add_command(eve)
bot.add_command(leave)

#///////////////////////////////////////////////////// GTTS /////////////////////////////////////////////////////

bot.add_command(eveth)
bot.add_command(eveen)
bot.add_command(translate)
bot.add_command(translate_JP)

#///////////////////////////////////////////////////// TARROT /////////////////////////////////////////////////////

bot.add_command(tarot)

#///////////////////////////////////////////////////// blackjack /////////////////////////////////////////////////////

bot.add_command(blackjack)
bot.add_command(hit)
bot.add_command(stand)

#///////////////////////////////////////////////////// blackjack /////////////////////////////////////////////////////

bot.add_command(fimport_sheet)
bot.add_command(fcharacter)
bot.add_command(fall)
bot.add_command(fgame)

#///////////////////////////////////////////////////// D&D /////////////////////////////////////////////////////
bot.add_command(roll)

bot.add_command(import_character)
bot.add_command(character)
bot.add_command(character_list)
bot.add_command(show_all_character_info)

server_on()

# เริ่มต้นการทำงานของบอท
bot.run(TOKEN)

