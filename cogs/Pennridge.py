import discord
from discord.ext import commands
import json

with open('Self_role.json') as f:
    sr = json.load(f)


class Pennridge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = f"{payload.channel_id}/{payload.message_id}"
        if message in sr:
            server = self.client.get_guild(616076450424029258)
            member = server.get_member(payload.user_id)
            for key in sr[message]:
                if key == payload.emoji.name or key == "Default_role":
                    chosen_role = discord.utils.get(server.roles, name=sr[message][key])
                    if "Inverted" in sr[message]:
                        await member.remove_roles(chosen_role, reason="Self assigned")
                    else:
                        await member.add_roles(chosen_role, reason="Self assigned")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message = f"{payload.channel_id}/{payload.message_id}"
        if message in sr:
            server = self.client.get_guild(616076450424029258)
            member = server.get_member(payload.user_id)
            for key in sr[message]:
                if key == payload.emoji.name or key == "Default_role":
                    chosen_role = discord.utils.get(server.roles, name=sr[message][key])
                    await member.remove_roles(chosen_role, reason="Self assigned")


def setup(client):
    client.add_cog(Pennridge(client))
