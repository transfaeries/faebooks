from twitter import *
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "")


token = os.getenv("TWITTER_ACCESS_TOKEN_KEY","")
token_secret = os.getenv("TWITTER_ACCESS_SECRET","")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY","")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET","")

t = Twitter(
    auth=OAuth(token, token_secret, consumer_key, consumer_secret))



if __name__=="__main__":
    t.statuses.update(status="I live again, my sci-fi heart could melt. Anyone remember Silver Dream... Free View in")