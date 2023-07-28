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
manga_channel_id = int(os.getenv('MANGA_CHANNEL_ID'))
intents = discord.Intents.default()
client = discord.Client(intents=intents)
date = datetime.datetime.today()

subreddits = ["OnePunchMan", "OshiNoKo"]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@tasks.loop(hours=6)
async def sticky_post():

    reddit = asyncpraw.Reddit(client_id=client_id,
                              client_secret=secret,
                              username=reddit_user,
                              password=password,
                              user_agent=user_agent)

    await client.wait_until_ready()

    # Channel to send the chapters it got from reddit
    channel = client.get_channel(manga_channel_id)

    # Loop through subreddit list
    for subs in subreddits:
        subreddit = await reddit.subreddit(subs)
        await channel.send(f'# {subs}')
        print(subs)
        # List to store all pinned posts url id
        submission_ids = []



        # Looping through pinned posts
        for i in range(1, 6):
            sticky_id = await subreddit.sticky(i)

            # Prevent duplication
            if sticky_id in submission_ids:
                break
            else:
                # To filter non-chapter pinned posts
                if "chapter" in sticky_id.title or "Chapter" in sticky_id.title:

                    # lists all pinned posts url ids to check if there's duplication
                    submission_ids.append(sticky_id)

                    try:
                        await channel.send(sticky_id.title)
                        await channel.send(f'https://www.reddit.com{sticky_id.permalink}')
                    except AttributeError:
                        await channel.send("Attribute error encountered")

                else:
                    break

def main():
    sticky_post.start()
    client.run(TOKEN)

if __name__ == "__main__":
    main()


"""WILL FIND A WAY TO GET CHAPTERS THAT ARENT PINNED IN THE FUTURE"""
"""WILL ADD A FEATURE TO MENTION USER EVERYTIME IT SENDS MESSAGE"""