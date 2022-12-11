# bot.py
import os

import discord
from dotenv import load_dotenv
import random
# from discord_analysis.ml.scripts.classify_pipeline import ClassificationPipeline
from discord_analysis.ml.scripts.bilstm import predict
from discord_analysis.firebase.db.realtime_db import RealtimeDB
from discord_analysis.streaming.kafka import KafkaHandler
from datetime import datetime
from multiprocessing import Process
from threading import Thread
import json

# classifier = ClassificationPipeline()
db = RealtimeDB(os.getenv("FIREBASE_DB_URL"))
kafka = KafkaHandler()

current_sentiment = {}


def sentiment(text):
    result = predict(text)
    print(text, " ", result)
    return result

load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.all())



def on_message_handler(msgID, text):
    global current_sentiment

    print("Handling message " + str(msgID))
    current_sentiment[msgID] = predict(text)



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

    consume_process = Thread(target=kafka.consume, kwargs={
        "topic": "zfzdjzcz-discord",
        "on_message_handler" : on_message_handler
    })
    consume_process.start()


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

    data = {
        "msgID" : message.id,
        "text" : text
    }
    kafka.produce("zfzdjzcz-discord", json.dumps(data))

    # text_sentiment = sentiment(text)

  

    while message.id not in current_sentiment:
        pass
    
    if current_sentiment[message.id] in ['Hate', 'Offensive']:
        await message.add_reaction("😡")
    else:
        await message.add_reaction("❤️")

    db.push({
        "user" : message.author.name,
        'channel': message.channel.name,
        "content": message.content,
        "sentiment":current_sentiment[message.id],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, "/server/message_log")
    


client.run(TOKEN)