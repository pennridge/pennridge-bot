import discord
from discord.ext import commands
import time
import os

token = 'NTYyMzgxNzQ0Nzg3OTQ3NTQy.XLE7dQ.oQWH4wwwKPmSzQeImWsTIjWkVsQ'
client = commands.Bot(command_prefix='~')

client.remove_command('help')

@client.event
async def on_ready():
    print('Bot running')
#    print(discord.__version__)
    game = discord.Game("~help")
    await client.change_presence(status=discord.Status.online, activity=game)
    

for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            client.load_extension(cog)
        except Exception as e:
            print(f'{cog} has big gay')
            raise e
        

client.run(token)
