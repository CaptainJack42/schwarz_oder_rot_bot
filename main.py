import os
import discord
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ.get('API_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to: \n',
            f'{guild.name} (id: {guild.id})'
        )

if __name__ == '__main__':
    print(API_TOKEN)
    client.run(API_TOKEN)
