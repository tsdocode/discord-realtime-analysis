# bot.py
import os

import discord
from dotenv import load_dotenv
import random
# from discord_analysis.ml.scripts.classify_pipeline import ClassificationPipeline
from discord_analysis.ml.scripts.bilstm import predict
from discord_analysis.firebase.db.realtime_db import RealtimeDB
from datetime import datetime

# classifier = ClassificationPipeline()
db = RealtimeDB(os.getenv("FIREBASE_DB_URL"))

def sentiment(text):
    result = predict(text)
    print(text, " ", result)
    return result

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.all())



@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    channel = client.get_channel(962051038548983871)
    await channel.send('Chú chó văn hoá is backkkk  :person_tipping_hand:')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_guild_channel_create(channel):
    db.save({
        "number_of_channels" : len(list(client.get_all_channels()))
    }, "server/channels")

@client.event
async def on_guild_channel_delete(channel):
    db.save({
        "number_of_channels" : len(list(client.get_all_channels()))
    }, "server/channels")


@client.event
async def on_member_join(member):
    print(f'{member.guild.member_count} member in server')
    db.save({
        'number_of_members' : member.guild.member_count
    }, "server/members")

@client.event
async def on_member_remove(member):
    db.save({
        'number_of_members' : member.guild.member_count
    }, "server/members")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '':
        return
    if '--clear all' in message.content:
        deleted = await message.channel.purge(limit=10000)
        return
    text = message.content.lower()
    text_sentiment = sentiment(text)

    db.push({
        "user" : message.author.name,
        'channel': message.channel.name,
        "content": message.content,
        "sentiment":text_sentiment,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, "/server/message_log")
    
    if text_sentiment in ['Hate', 'Offensive']:
        await message.add_reaction("😡")
        # mention = message.author.mention
        # await message.channel.send(f"{mention} nói bậy là bị ban nhe <3")
        
        # await message.delete()
    else:
        await message.add_reaction("❤️")


client.run(TOKEN)