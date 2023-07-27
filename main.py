import discord
import asyncpraw
from discord.ext import tasks
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('client_id')
secret = os.getenv('secret')
user_agent = os.getenv('user_agent')
reddit_user = os.getenv('reddit_user')
password = os.getenv('password')
TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
date = datetime.datetime.today()

subreddits = ["OnePunchMan", "OshiNoKo"]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@tasks.loop(hours=4)
async def opm():
    # date = datetime.datetime.today()
    day = int(datetime.datetime.today().strftime('%w'))

    if day == 0:

        reddit = asyncpraw.Reddit(client_id=client_id,
                                  client_secret=secret,
                                  username=reddit_user,
                                  password=password,
                                  user_agent=user_agent)

        subreddit = await reddit.subreddit("Manga")
        all_subs = []
        top = subreddit.top(time_filter="month")
        async for submission in top:
            if f"[DISC] One Punch" in submission.title:
                all_subs.append(f"{submission.title} - {submission.url}\n")

        channel = client.get_channel(993091036572303420)


        await channel.purge(limit=10)
        for subs in all_subs:
            await channel.send(subs)

@tasks.loop(hours=4)
async def sticky_post():

    reddit = asyncpraw.Reddit(client_id=client_id,
                              client_secret=secret,
                              username=reddit_user,
                              password=password,
                              user_agent=user_agent)

    subreddit = await reddit.subreddit("OnePunchMan")
    all_subs = []
    sticky_id = await subreddit.sticky()
    print(sticky_id.permalink)



@tasks.loop(hours=4)
async def kaguya():
    # date = datetime.datetime.today()
    day = int(datetime.datetime.today().strftime('%w'))

    if day == 0:

        reddit = asyncpraw.Reddit(client_id=client_id,
                                  client_secret=secret,
                                  username=reddit_user,
                                  password=password,
                                  user_agent=user_agent)

        subreddit = await reddit.subreddit("Manga")
        all_subs = []
        top = subreddit.top(time_filter="month")
        async for submission in top:
            if f"[DISC] Kaguya" in submission.title:
                all_subs.append(f"{submission.title} - {submission.url}\n")

        channel = client.get_channel(993091063407448134)


        await channel.purge(limit=10)
        for subs in all_subs:
            await channel.send(subs)


def main():
    # kaguya.start()
    # opm.start()
    sticky_post.start()
    client.run(TOKEN)


if __name__ == "__main__":
    main()



