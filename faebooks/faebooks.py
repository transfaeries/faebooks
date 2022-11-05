## Good Morning, welcome to faebot
# Faebot's is a bot who is also a faerie
#Faebot uses Open.ai gpt to generate tweets as well as have conversations on twitter

# Faebot will post a new tweet at random intervals during the day 

import os
import sys
import time
import logging
from random import randrange
from twitter import *
import openai
import asyncio
import signal

# set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')



# This will seed the model:
tweet_prompt = ""
model = os.getenv("MODEL_NAME", "curie")



class Faebooks:
    def __init__(self) -> None:
        # this loads all of the secrets
        openai.api_key = os.getenv("OPENAI_API_KEY", "")
        token = os.getenv("TWITTER_ACCESS_TOKEN","")
        token_secret = os.getenv("TWITTER_ACCESS_SECRET","")
        api_key = os.getenv("TWITTER_API_KEY","")
        api_secret = os.getenv("TWITTER_API_SECRET","")

        #set up the twitter connection
        self.twitter = Twitter(
            auth=OAuth(token, token_secret, api_key, api_secret))



    #Prompts Open AI for a tweet
    def generate(prompt: str = "") -> str:
        response = openai.Completion.create(  # type: ignore
            engine=model,
            prompt=prompt,
            temperature=0.7,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.99,
            presence_penalty=0.3,
            stop=["\n\n"],
        )
        return response["choices"][0]["text"].strip()

    async def tweet(self) -> None:
        """This will generate a tweet based on the prompt and post it to twitter"""
        tweet = self.generate(prompt=tweet_prompt)
        logging.info(f"Tweeting: {tweet}")
        self.twitter.statuses.update(status=tweet)

    sigints = 0

    async def start(self) -> None:
        """This will start the asyncio running loop and set the signint handlers"""
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.sync_signal_handler)
        loop.add_signal_handler(signal.SIGTERM, self.sync_signal_handler)
        restart_count = 0
        max_backoff = 15
        while self.sigints == 0 and not self.exiting:
            # try:
            #     await self.tweet()
            #     await asyncio.sleep(60 * 60 * 24)
            # except Exception as e:
            #     logging.error(e)
            #     backoff = 2 ** restart_count
            #     logging.info("backing off for %s seconds", backoff)
            #     await asyncio.sleep(backoff)
            #     restart_count += 1

            logging.info(
                "started faebot @ faebot_01"
            )
    


    # def sync_signal_handler(self, *_: Any) -> None:
    #     """Try to start async_shutdown and/or just sys.exit"""
    #     logging.info("handling sigint. sigints: %s", self.sigints)
    #     self.sigints += 1
    #     self.exiting = True
    #     try:
    #         loop = asyncio.get_running_loop()
    #         logging.info("got running loop, scheduling async_shutdown")
    #         asyncio.run_coroutine_threadsafe(self.async_shutdown(), loop)
    #     except RuntimeError:
    #         asyncio.run(self.async_shutdown())
    #     if self.sigints >= 3:
    #         sys.exit(1)

    async def async_shutdown(self) -> None:
        """Shutdown the bot"""
        logging.info("shutting down")
        await self.twitter.close()
        await self.session.close()
        sys.exit(0)

    



if __name__=="__main__":
    faebot = Faebooks()
    asyncio.run(faebot.start())