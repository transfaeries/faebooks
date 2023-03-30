## Good Morning, welcome to faebot
# Faebot's is a bot who is also a faerie
# Faebot uses Open.ai gpt to generate posts as well as have conversations

# Faebot will post a new post at random intervals during the day

import os
import sys
import time
import logging
from random import randrange
from twitter import *
from mastodon import Mastodon
import openai
import asyncio
import signal

# set up logging
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


# This will seed the model:
post_prompt = ""
model = os.getenv("MODEL_NAME", "curie")


class Faebooks:
    def __init__(self) -> None:
        # this loads all of the secrets
        openai.api_key = os.getenv("OPENAI_API_KEY", "")
        token = os.getenv("TWITTER_ACCESS_TOKEN", "")
        token_secret = os.getenv("TWITTER_ACCESS_SECRET", "")
        api_key = os.getenv("TWITTER_API_KEY", "")
        api_secret = os.getenv("TWITTER_API_SECRET", "")
        masto_token = os.getenv("MASTO_ACCESS_TOKEN", "")
        masto_url = os.getenv("MASTO_BASE_URL", "")

        # set up the twitter connection
        self.twitter = Twitter(auth=OAuth(token, token_secret, api_key, api_secret))

        # set up the mastodon connection
        self.mastodon = Mastodon(access_token=masto_token, api_base_url=masto_url)

        # additional setup
        self.exiting = False
        self.sigints = 0

    # Prompts Open AI for a post
    async def generate(self, prompt: str = "") -> str:
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

    async def post(self) -> None:
        """This will generate a post based on the prompt and post it to twitter and mastodon"""
        post = await self.generate(post_prompt)
        logging.info(f"posting: {post}")
        self.twitter.statuses.update(status=post)
        self.mastodon.toot(post)

    async def start(self) -> None:
        """This will start the asyncio running loop and set the signint handlers"""
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.sync_signal_handler)
        loop.add_signal_handler(signal.SIGTERM, self.sync_signal_handler)
        restart_count = 0
        max_restarts = 15
        while self.sigints == 0 and not self.exiting:
            try:
                await self.post()
                sleeptime = randrange(3000, 17200)
                logging.info(f"sleeping for {sleeptime} seconds before posting again.")
                await asyncio.sleep(sleeptime)

            except Exception as e:
                logging.error(e)
                backoff = 2**restart_count
                if restart_count >= max_restarts:
                    logging.error("max restarts reached, exiting")
                    sys.exit(1)
                logging.info("backing off for %s seconds", backoff)
                await asyncio.sleep(backoff)
                restart_count += 1

            logging.info("started faebot @ faebot_01")

    def sync_signal_handler(self, *_: any) -> None:
        """Try to start async_shutdown and/or just sys.exit"""
        logging.info("handling sigint. sigints: %s", self.sigints)
        self.sigints += 1
        self.exiting = True
        try:
            loop = asyncio.get_running_loop()
            logging.info("got running loop, scheduling async_shutdown")
            asyncio.run_coroutine_threadsafe(self.async_shutdown(), loop)
        except RuntimeError:
            asyncio.run(self.async_shutdown())
        if self.sigints >= 3:
            sys.exit(1)

    async def async_shutdown(self) -> None:
        """Shutdown the bot"""
        logging.info("shutting down")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        sys.exit(0)


if __name__ == "__main__":
    faebot = Faebooks()
    asyncio.run(faebot.start())
