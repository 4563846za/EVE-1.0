import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, Member
from gtts import gTTS
from googletrans import Translator

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

eve_icon = 'https://media.discordapp.net/attachments/1012033549207076894/1242194388516601980/IMG_0398z.png?ex=664eed6d&is=664d9bed&hm=6a6c42bc54cba0418926c83ff4d3bdc1958a8355cae7655d0d8dad48091b27b2&=&format=webp&quality=lossless&width=701&height=701'
eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_icons = 'https://media.discordapp.net/attachments/1012033549207076894/1242894958814433370/IMG_0500.png?ex=664f7fa2&is=664e2e22&hm=22b48fa5edd5a831350d04aedb12758cd3b316311982f1cfe3ebb6cdddedaa94&=&format=webp&quality=lossless&width=377&height=350'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'

@bot.command(pass_context=True, aliases=['eth'])
async def eveth(ctx, *, text):
    language = 'th'
    output = gTTS(text=text, lang=language, slow=False, lang_check=True)
    output.save('voice.mp3')
    source = FFmpegPCMAudio('voice.mp3')
    player = ctx.guild.voice_client.play(source)

@bot.command(pass_context=True, aliases=['een'])
async def eveen(ctx, *, text):
    language = 'en'
    output = gTTS(text=text, lang=language, slow=False, lang_check=True)
    output.save('voice.mp3')
    source = FFmpegPCMAudio('voice.mp3')
    player = ctx.guild.voice_client.play(source)



def translate_text(text, dest_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text


@bot.command(pass_context=True, aliases=['th'])
async def translate(ctx, *, text, user: Member=None):
    if user is None:
        user = ctx.message.author

        tr = translate_text(text, dest_language='th')
        embed = discord.Embed(title="EVE Translator")
        embed.add_field(name="คำแปล",value=f"```{tr}```")
        embed.set_author(name=f"EVE", icon_url=eve_icon)
        embed.set_footer(text=eve_footer, icon_url=eve_iconf)
        embed.set_thumbnail(url=user.display_avatar)
        await ctx.send(embed=embed)

        language = 'th'
        output = gTTS(text=tr, lang=language, slow=False, lang_check=True)    
        output.save('voice.mp3')
        source = FFmpegPCMAudio('voice.mp3')
        player = ctx.guild.voice_client.play(source)




@bot.command(pass_context=True, aliases=['jp'])
async def translate_JP(ctx, *, text, user: Member=None):
    if user is None:
        user = ctx.message.author

        tr = translate_text(text, dest_language='ja')
        embed = discord.Embed(title="EVE Translator")
        embed.add_field(name="คำแปล",value=f"```{tr}```")
        embed.set_author(name=f"EVE", icon_url=eve_icon)
        embed.set_footer(text=eve_footer, icon_url=eve_iconf)
        embed.set_thumbnail(url=user.display_avatar)
        await ctx.send(embed=embed)

        language = 'ja'
        output = gTTS(text=tr, lang=language, slow=False, lang_check=True)    
        output.save('voice.mp3')
        source = FFmpegPCMAudio('voice.mp3')
        player = ctx.guild.voice_client.play(source)