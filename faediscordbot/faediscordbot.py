## Faediscordbot is a general purpose discord bot using discord.py which reads and responds to messages on a discord server.

import discord
import asyncio
import random
import logging
import openai

logging.basicConfig(level=logging.INFO)

class MyClient(discord.Client):
    
    async def on_ready(self):
        """runs when bot is ready"""
        logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
        logging.info("------")

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('token')


