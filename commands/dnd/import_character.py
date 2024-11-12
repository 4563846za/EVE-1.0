import discord
import json
import re
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

eve_iconf = 'https://media.discordapp.net/attachments/1012033549207076894/1240339785692745819/Untitled-1-Recovered.png?ex=664633f1&is=6644e271&hm=8b363d2e40c166d5793139a768fee49c42af52212ceffe5f74820fc222905658&=&format=webp&quality=lossless&width=701&height=701'
eve_footer ='EVE Bot | อิฐอุ๋ง | Discord:@itoung | !help'

def update_character_sheet(character_id):
    url = f"https://character-service.dndbeyond.com/character/v5/character/{character_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        character_data = response.json()

        if character_data['success']:
            character = character_data['data']
            
            character_sheet = {
                'id': character['id'],
                'user_id': character['userId'],
                'username': character['username'],
                'is_assigned_to_player': character['isAssignedToPlayer'],
                'readonly_url': character['readonlyUrl'],
                'avatar_url': character['decorations']['avatarUrl'],
                'frame_avatar_url': character['decorations']['frameAvatarUrl'],
                'small_backdrop_avatar_url': character['decorations']['smallBackdropAvatarUrl'],
                'large_backdrop_avatar_url': character['decorations']['largeBackdropAvatarUrl'],
                'name': character['name'],
                'social_name': character['socialName'],
                'gender': character['gender'],
                'faith': character['faith'],
                'age': character['age'],
                'hair': character['hair'],
                'eyes': character['eyes'],
                'skin': character['skin'],
                'height': character['height'],
                'weight': character['weight'],
                'inspiration': character['inspiration'],
                'base_hit_points': character['baseHitPoints'],
                'stats': {stat['id']: stat['value'] for stat in character['stats']},
                'background_name': character['background']['definition']['name'],
                'background_description': character['background']['definition']['description'],
                'race_full_name': character['race']['fullName'],
                'race_description': character['race']['description'],
                'inventory': [{
                    'item_id': item['id'],
                    'item_name': item['definition']['name'],
                    'item_type': item['definition']['type'],
                    'equipped': item['equipped']
                } for item in character['inventory']],
                'notes_allies': character['notes']['allies'],
                'notes_personal_possessions': character['notes']['personalPossessions'],
                'personality_traits': character['traits']['personalityTraits'],
                'ideals': character['traits']['ideals'],
                'bonds': character['traits']['bonds'],
                'flaws': character['traits']['flaws'],
                'use_homebrew_content': character['preferences']['useHomebrewContent']
            }

            return character_sheet
        else:
            raise Exception("Failed to update character sheet.")
    except requests.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

@bot.command(name="import_character", pass_context=True, aliases=['import'])
async def import_character(ctx, character_url: str):
    match = re.search(r"characters/(\d+)", character_url)
    if not match:
        await ctx.send("URL ไม่ถูกต้อง กรุณาลองใหม่")
        return
    
    character_id = match.group(1)
    try:
        character_sheet = update_character_sheet(character_id)
        user_id = str(ctx.author.id)

        # เปิดไฟล์และตรวจสอบคีย์ 'characters'
        with open("characters.json", "r+") as file:
            data = json.load(file)

            # หากไม่มีข้อมูลของผู้ใช้ให้สร้างข้อมูลใหม่
            if user_id not in data:
                data[user_id] = {"characters": [], "active_character": None}

            if any(char['id'] == character_sheet['id'] for char in data[user_id]["characters"]):
                await ctx.send("ตัวละครนี้ถูกเพิ่มแล้ว.")
                return

            # ทำให้ตัวละครที่เพิ่งเพิ่มเป็นตัวละครหลัก
            data[user_id]["characters"].append(character_sheet)
            data[user_id]["active_character"] = character_sheet['name']

            file.seek(0)
            json.dump(data, file, indent=4)
        
        await ctx.send(f"ตัวละคร {character_sheet['name']} ถูกเพิ่มและตั้งเป็นตัวละครหลักเรียบร้อย!")
    except Exception as e:
        await ctx.send(f"เกิดข้อผิดพลาด: {e}")