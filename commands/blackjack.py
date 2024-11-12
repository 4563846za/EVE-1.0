import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


suits = ['♡', '♢', '♣', '♠']
ranks = [':two:', '3', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:', ':regional_indicator_j:', ':regional_indicator_q:', ':regional_indicator_k:', ':a:']
values = {':two:': 2, '3': 3, ':four:': 4, ':five:': 5, ':six:': 6, ':seven:': 7, ':eight:': 8, ':nine:': 9, ':keycap_ten:': 10, ':regional_indicator_j:': 10, ':regional_indicator_q:': 10, ':regional_indicator_k:': 10, ':a:': 11}


eve_icon = 'https://media.discordapp.net/attachments/1012033549207076894/1242194388516601980/IMG_0398z.png?ex=664eed6d&is=664d9bed&hm=6a6c42bc54cba0418926c83ff4d3bdc1958a8355cae7655d0d8dad48091b27b2&=&format=webp&quality=lossless&width=701&height=701'
eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_icons = 'https://media.discordapp.net/attachments/1012033549207076894/1242894958814433370/IMG_0500.png?ex=664f7fa2&is=664e2e22&hm=22b48fa5edd5a831350d04aedb12758cd3b316311982f1cfe3ebb6cdddedaa94&=&format=webp&quality=lossless&width=377&height=350'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'


class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        rank, suit = card
        self.value += values[rank]
        if rank == ':a:':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def start_game(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

    def hit(self, hand):
        hand.add_card(self.deck.deal())

    def get_hand_value(self, hand):
        return hand.value

    def display_hand(self, hand, hide_dealer_card=False):
        hand_display = []
        for idx, card in enumerate(hand.cards):
            if hide_dealer_card and idx == 0:
                hand_display.append("จั่ว")
            else:
                hand_display.append(f"{card[0]} {card[1]}")
        return "  ,  ".join(hand_display)

game = None

@bot.command()
async def blackjack(ctx):
    global game
    game = BlackjackGame()
    game.start_game()
    start =discord.Embed(title=f'เริ่มเล่นเกมแห่งความมืด Blackjack')
    player =discord.Embed(title=f'ไพ่บนมือของคุณ', description=f"{game.display_hand(game.player_hand)} = ``{game.get_hand_value(game.player_hand)}``", color=0x00ff00)
    player.set_footer(text='!blackjack, !hit, !stand', icon_url=eve_iconf)
    dealer =discord.Embed(title=f'มือเจ้า', description=f"{game.display_hand(game.dealer_hand)} = ``{game.get_hand_value(game.dealer_hand)}``", color=0x00ff00)
    await ctx.send(embed=start)    
    await ctx.send(embed=dealer)
    await ctx.send(embed=player)

@bot.command()
async def hit(ctx):
    global game
    if game:
        game.hit(game.player_hand)
        player = discord.Embed(title=f'ไพ่บนมือของคุณ', description=f"{game.display_hand(game.player_hand)} = ``{game.get_hand_value(game.player_hand)}``", color=0x00ff00)
        player.set_footer(text='!blackjack, !hit, !stand', icon_url=eve_iconf)        
        dealer = discord.Embed(title=f'เจ้ากินเรียบ ไม่นับไพ่ดีๆก็งี้แหละ', color=0x00ff00)
        dealer.set_footer(text='เริ่มใหม่กด !blackjack', icon_url=eve_iconf)
        dealer.set_image(url='https://cdn.discordapp.com/attachments/1253978000610033736/1253983438906720357/IMG_0500.png?ex=6677d695&is=66768515&hm=c64338f22a6146b7198f774dad8c8b4885ab3593fea57770065c7b5efb5e886c&')
        await ctx.send(embed=player)
        if game.get_hand_value(game.player_hand) > 21:
            await ctx.send(embed=dealer)
            game = None
    else:
        await ctx.send("เริ่มตาใหม่กด !blackjack")

@bot.command()
async def stand(ctx):
    global game
    if game:
        while game.get_hand_value(game.dealer_hand) < 17:
            game.hit(game.dealer_hand)
        dealer_value = game.get_hand_value(game.dealer_hand)
        player_value = game.get_hand_value(game.player_hand)
        dealer = discord.Embed(title=f'มือเจ้า', description=f"{game.display_hand(game.dealer_hand)} = ``{game.get_hand_value(game.dealer_hand)}``", color=0x00ff00)
        await ctx.send(embed=dealer)
        if dealer_value > 21 or player_value > dealer_value:
            win = discord.Embed(title=f'โกง โกงแน่ๆ แกโกงใช่มั้ย!!', color=0x00ff00)
            win.set_footer(text='เริ่มใหม่กด !blackjack', icon_url=eve_iconf)
            win.set_image(url='https://media.discordapp.net/attachments/1253978000610033736/1253982245652529253/IMG_0482.png?ex=6677d579&is=667683f9&hm=c55c6db96dc90694655753a8d31d77bd016c1cbafd289a70923538bdae9aff7d&=&format=webp&quality=lossless&width=684&height=700')
            await ctx.send(embed=win)
        elif player_value == dealer_value:
            draw = discord.Embed(title=f'ทำไพ่ปะเนี่ย', color=0x00ff00)
            draw.set_footer(text='เริ่มใหม่กด !blackjack', icon_url=eve_iconf)
            draw.set_image(url='https://media.discordapp.net/attachments/1253978000610033736/1253984540985131130/IMG_0484.png?ex=6677d79c&is=6676861c&hm=21628015e1b8d6070a7a6fe3be855b88e100f2d2e0200458c78581fee23c3946&=&format=webp&quality=lossless&width=686&height=701')
            await ctx.send(embed=draw)  
        else:
            lose = discord.Embed(title=f'ไปหัดมาใหม่นะ', color=0x00ff00)
            lose.set_footer(text='เริ่มใหม่กด !blackjack', icon_url=eve_iconf)
            lose.set_image(url='https://media.discordapp.net/attachments/1253978000610033736/1253983438906720357/IMG_0500.png?ex=6677d695&is=66768515&hm=c64338f22a6146b7198f774dad8c8b4885ab3593fea57770065c7b5efb5e886c&=&format=webp&quality=lossless&width=754&height=701')
            await ctx.send(embed=lose)    
        game = None
    else:
        await ctx.send("เริ่มตาใหม่กด !blackjack")