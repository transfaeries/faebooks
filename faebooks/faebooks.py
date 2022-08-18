## Good Morning, welcome to faebot
# Faebot's is a bot who is also a faerie
#Faebot uses Open.ai gpt to generate tweets as well as have conversations on twitter

import os
import time
import logging
from random import randrange
from twitter import *
import openai

# set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# this loads all of the secrets
openai.api_key = os.getenv("OPENAI_API_KEY", "")
token = os.getenv("TWITTER_ACCESS_TOKEN","")
token_secret = os.getenv("TWITTER_ACCESS_SECRET","")
api_key = os.getenv("TWITTER_API_KEY","")
api_secret = os.getenv("TWITTER_API_SECRET","")
model = os.getenv("MODEL_NAME", "curie")

#set up the twitter connection
t = Twitter(
    auth=OAuth(token, token_secret, api_key, api_secret))

# This will seed the model:
tweet_prompt = "The following is a tweet by faebot_01, a bot that is also a faerie:"

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

if __name__=="__main__":
    ## start a python thread for the main load of generating and posting tweets
    
   
   
    # while True:
    #     message = generate(tweet_prompt)
    #     logging.info("MESSAGE TO POST: "+message)
    #     t.statuses.update(status=message)
    #     # sleep for 5 mins to 2 hours before posting again
    #     sleeptime=randrange(300,7200)
    #     logging.info(f"sleeping for {sleeptime} seconds before posting again.")
    #     time.sleep(sleeptime)