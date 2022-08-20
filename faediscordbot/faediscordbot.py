## Faediscordbot is a general purpose discord bot using discord.py which reads and responds to messages on a discord server.

import discord
import asyncio
import random
import os
import logging
import openai

openai.api_key = os.getenv("OPENAI_API_KEY", "")
model = os.getenv("MODEL_NAME", "text-curie-001")

# set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class Faebot(discord.Client):
    
    async def on_ready(self):
        """runs when bot is ready"""
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logging.info("------")

    async def on_message(self, message):
        """Handles what happens when the bot receives a message"""
        # don't respond to ourselves
        if message.author == self.user:
            return

        #prevent bot from replying too quickly

        #when we're ready for the bot to reply, feed the context to OpenAi and return the response
        prompt = ("The Following is a conversation with an AI chatbot known as faebot. \n"
                  "Faebot is young curious and loves nature, it is a faerie as well as a robot.\n"
                  f"{message.author}: {message.content}")
        # import pdb;pdb.set_trace()
        logging.info(f"PROMPT = {prompt}")
        reply = await self.generate(prompt, model)
        logging.info(f"Received response: {reply}")
        if not reply:
            reply = "I don't know what to say"
        return await message.channel.send(reply)

    async def generate(self, prompt: str = "", engine = "text-curie-001") -> str:
        response = openai.Completion.create(  # type: ignore
            engine=engine,
            prompt=prompt,
            temperature=0.7,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.99,
            presence_penalty=0.3,
            stop=["\n"],
        )
        return response["choices"][0]["text"].strip()


if __name__=="__main__":
    intents = discord.Intents.default()
    # intents.message_content = True
    bot = Faebot(intents=intents)
    bot.run(os.environ["DISCORD_TOKEN"])


