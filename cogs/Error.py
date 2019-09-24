import discord
from discord.ext import commands
import random
import time
import json

file_directory = "C:/Users/Howdy/Desktop/Coding/Bots/I'm very sorry/Data.txt"

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open(file_directory, 'r') as f:
            self.data = json.load(f)
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("I don't know what that command is")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: missing argument")
        else:
            try:
                await ctx.send("Unforeseen error happened, this is a bruh moment")
            except discord.Forbidden:
                pass
            print(f"Error raised {ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}")
            raise error



def setup(client):
    client.add_cog(error(client))
