
import discord
from discord.ext import commands
import asyncio
import urllib.parse, urllib.request
from discord.utils import get
from discord import Member

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())


eve_icon = 'https://media.discordapp.net/attachments/1012033549207076894/1242194388516601980/IMG_0398z.png?ex=664eed6d&is=664d9bed&hm=6a6c42bc54cba0418926c83ff4d3bdc1958a8355cae7655d0d8dad48091b27b2&=&format=webp&quality=lossless&width=701&height=701'
eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'



@bot.command(pass_context=True, aliases=['e'])
async def eve(ctx):
    file_path = 'EVE Hello.mp3'
    channel = ctx.author.voice.channel

    if not channel:
        return print('Invalid voice channel ID.')

    voice_client = await channel.connect()

    while True:
        voice_client.play(discord.FFmpegPCMAudio(file_path))
        await asyncio.sleep(voice_client.source.duration)
        voice_client.stop()



@bot.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        print(f'EVE ออกจากห้องเสียง{channel}แล้ว')
        await ctx.send('งั้นฉันไปละนะ')
    else:
        await ctx.send('EVE ออกจากห้องเสียง{channel}แล้ว | !help')


@bot.command(pass_context=True, aliases=['pro'])
async def profile(ctx, user: Member=None):

    if user is None:
        user = ctx.message.author

    inline = True
    emmbed = discord.Embed(title='ข้อมูลเบื้องต้นของ'f' {user.display_name}', color=0x66FFFF)
    userData = {
        'Name' : user.mention,
        'Role' : user.top_role,
        'Server' : user.guild,
        'Status': user.status
    }
    for [fieldName, fieldVal] in userData.items():
        emmbed.add_field(name=fieldName, value=fieldVal, inline=inline)
    emmbed.set_thumbnail(url=user.display_avatar)
    emmbed.set_image(url=user.display_avatar)
    emmbed.set_author(name=f"EVE", icon_url=eve_icon)
    emmbed.set_footer(text=eve_footer, icon_url=eve_iconf)

    await ctx.send(embed=emmbed)


@bot.command(pass_context=True, aliases=['k', 'ki'])
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command(pass_context=True, aliases=['ba'])
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)