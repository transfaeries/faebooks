from twitter import *
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "")


token = os.getenv("TWITTER_ACCESS_TOKEN_KEY","")
token_secret = os.getenv("TWITTER_ACCESS_SECRET","")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY","")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET","")
model = os.getenv("MODEL_NAME", "curie")

t = Twitter(
    auth=OAuth(token, token_secret, consumer_key, consumer_secret))

tweet_prompt = "The following is a tweet by faebot, a bot that is also a faerie:"

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
    # t.statuses.update(status="I live again, my sci-fi heart could melt. Anyone remember Silver Dream... Free View in")
    message = generate(tweet_prompt)
    print(message)
    t.statuses.update(status=message)