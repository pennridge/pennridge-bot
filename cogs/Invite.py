import discord
from discord.ext import commands
import json
import datetime
import re


class invite(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open('Data.json') as f:
            self.data = json.load(f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send("""hi:)))))
join `?rank Band` if your in band""")
        member_id = str(member.id)
        guild_id = str(member.guild.id)
        entrance = self.client.get_channel(616307480422645778)

        usedinvites = []
        if guild_id in self.data:
            for key in self.data[guild_id]["members"]:
                member_data = self.data[guild_id]["members"][key]
                for i in await entrance.invites():
                    if i.code in member_data["invites"]:
                        bruh = member_data["invites"][i.code]
                        if i.uses < bruh["real"] + bruh["fake"] + bruh["unaccounted"]:
                            usedinvites.append(i.code)
                            if member_id not in self.data[guild_id]:
                                bruh["real"] += 1
                            else:
                                bruh["fake"] += 1
        else:
            self.data[guild_id] = {}
            self.data[guild_id]["members"] = {}
            self.data[guild_id]["shop"] = {}
        if member not in self.data[guild_id]["members"]:
            self.data[guild_id]["members"][member] = {}
            self.data[guild_id]["members"][member]["joined with"] = usedinvites
            self.data[guild_id]["members"][member]["spent"] = 0
            self.data[guild_id]["members"][member]["invites"] = {}
        else:
            for i in usedinvites:
                self.data[guild_id]["members"][member]["joined with"].append(i)

        with open("Data.json", "w") as h:
            json.dump(self.data, h, indent=2)

    @commands.command()
    async def add(self, ctx):
        await ctx.send("yeaj")

    @commands.command(aliases=["create invite", "make invite", "makeinvite"], case_insensitive=True)
    async def createinvite(self, ctx):
        await ctx.send("test")
        entrance = self.client.get_channel(616307480422645778)
        guild_id = str(ctx.guild.id)
        member = str(ctx.author.id)

        if len(self.data[guild_id]["members"][member]["invites"]) < 4:
            await entrance.create_invite()
        else:
            await ctx.send("You have too many invites")
            return

        invites = []
        for i in await entrance.invites():
            if i.inviter == self.client.user:
                invites.append(i.code)
                for key in self.data[guild_id]["members"]:
                    if i.code in self.data[guild_id]["members"][key]["invites"]:
                        invites.remove(i.code)

        for code in invites:
            if len(self.data[guild_id]["members"][member]["invites"]) < 4:
                self.data[guild_id]["members"][member]["invites"][code] = {}
                h = self.data[guild_id]["members"][member]["invites"][code]
                h["real"] = 0
                h["fake"] = 0
                h["unaccounted"] = 0
                h["unwanted"] = 0
                await ctx.send(f"Done! Your invite is discord.gg/{code}")
            else:
                await ctx.send("You have too many invites")

        with open("Data.json", "w") as h:
            json.dump(self.data, h, indent=2)

    @commands.command(aliases=["delete invite", "del invite"], case_insensitive=True)
    async def deleteinvite(self, ctx, url: str):
        print(url)
        member_invites = self.data[str(ctx.guild.id)]["members"][str(ctx.author.id)]["invites"]
        if url in member_invites:
            try:
                await self.client.delete_invite(url)
            except discord.NotFound:
                pass

            self.data[str(ctx.guild.id)]["members"][str(ctx.author.id)]["spent"] -= member_invites[url]
            del member_invites[url]

            with open("Data.json", "w") as h:
                json.dump(self.data, h, indent=2)

            await ctx.send(f"invite **{url}** has been deleted")
        else:
            await ctx.send("you don't have that url")

    @commands.command()
    async def invites(self, ctx):
        invite = self.data[str(ctx.guild.id)]["members"][str(ctx.author.id)]["invites"]
        await ctx.send(json.dumps(invite, indent=2))

    @commands.command()
    async def shop(self, ctx):
        await ctx.send("yooo we got the shop")

    @commands.command()
    async def buy(self, ctx, request: str):
        guild_id = str(ctx.guild.id)
        member = str(ctx.author.id)
        total = 0

        item = None
        for i in self.data[guild_id]["shop"]:
            if request.lower().startswith(i):
                item = i

        if item is None:
            await ctx.send("Sorry, but you can't buy that")
            return

        for mmmm in self.data[guild_id]["members"][member]["invites"]:
            i = self.data[guild_id]["members"][member]["invites"][mmmm]
            total += i["real"]
            points = total - self.data[guild_id]["members"][member]["spent"]


        itemdata = self.data[guild_id]["shop"][item]
        price = itemdata * int(re.search(r'\d+', request).group())

        if points < itemdata["price"]:
            await ctx.send("You don't have enough points to get that")
            return
        else:

            self.data[guild_id]["members"][member]["spent"] += itemdata["price"]

            await ctx.send(f"you bought {self.data[guild_id]['shop'][item]}")

        await ctx.send(points)

    @add.before_invoke
    @createinvite.before_invoke
    @deleteinvite.before_invoke
    @invites.before_invoke
    @buy.before_invoke
    async def addmember(self, ctx):
        guild_id = str(ctx.guild.id)
        member = str(ctx.author.id)

        if guild_id not in self.data:
            self.data[guild_id] = {}
            self.data[guild_id]["members"] = {}
            self.data[guild_id]["shop"] = {}

        if member not in self.data[guild_id]["members"]:
            self.data[guild_id]["members"][member] = {}
            self.data[guild_id]["members"][member]["joined with"] = ["unaccounted"]
            self.data[guild_id]["members"][member]["spent"] = 0
            self.data[guild_id]["members"][member]["invites"] = {}
            self.data[guild_id]["members"][member]["inventory"] = {}
            self.data[guild_id]["members"][member]["effects"] = {}

        with open("Data.json", "w") as h:
            json.dump(self.data, h, indent=2)


def setup(client):
    client.add_cog(invite(client))
