import discord
from discord.ext import commands
import time
import difflib

Modrole = "Mod"
Grades = ['Freshman', 'Sophomore', 'Junior', 'Senior']
Subjects = ["math", "english", "social", "ss", "science", "languages"]


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ok(self, ctx):
        await ctx.send('ok')

    @commands.command()
    async def ping(self, ctx):
        start_time = time.time()
        await ctx.send('pinging...', delete_after=1)
        stop_time = time.time()
        ft1 = stop_time - start_time
        ft = '%.2f' % ft1
        await ctx.send(f'Pong! `{ft} secconds`')

    @commands.command(aliases=["h"], case_insensitive=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title="Commands",
            description="prefix is `~`",
            colour=discord.Colour.green()
        )
        embed.add_field(name="Miscellaneous", value="""**help** - nobody knows what this command does
**ping** - checks the ping of the bot
\u200b""")
        embed.add_field(name="economy", value="""
**shop** - list of things you can buy with points you get from inviting others
**create invite** - makes an invite you can gain points with
**delete invite** - deletes invite
**invites** - list of invites you have (warning, it's bad right now)
**send** - sends an amount of points to a user""", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def send(self, ctx, *, msg: str):
        global catehgory
        print("command recieved")
        if not ctx.message.channel.type == discord.ChannelType.private:
            await ctx.send("You should send it in a dm so it can't be traced", delete_after=6)
            return
        if msg.count(' ') < 1:
            await ctx.send("You need to have a message", delete_after=60)
            return
        chan, message = msg.split(' ', 1)
        for embed in ctx.message.attachments:
            message += f" {embed.url}"
        if len(message) > 2000:
            await ctx.send("Sorry, but when the url is included the message length is too long")
            return
        if "@everyone" in ctx.message.content:
            await ctx.send("I'm not gonna ping everyone retad :angjery:", delete_after=60)
            return

        guild = self.client.get_guild(616076450424029258)
        user = guild.get_member(ctx.author.id)
        log = self.client.get_channel(618125023932317726)


        check = "start"
        for role in user.roles:
            if role.name in Grades:
                if check == "start":
                    grade = str(role.name)
                    print(grade)
                    catehgory = discord.utils.get(guild.categories, name=grade)
                    check = "Grade found"
                else:
                    await ctx.send("sorry, but you have more than one grade role. Please remove it using `?rank`")
        print("grade found")
        if check == "Grade found":
            if chan.lower() in Subjects:
                check = "Channel found"
                if chan.lower() == "social":
                    message.replace(" studies", "")
                    chan = "social-studies"
                elif chan.lower() == "ss":
                    chan = "social-studies"
        print(check)
        possiblemsgobj = []
        for channel in guild.text_channels:
            if channel.name == chan.lower():
                if check == "Channel found":
                    if channel.category.name == catehgory.name:
                        print(catehgory.name)
                        await channel.send(message)

                        async for msgobj in channel.history(limit=10):
                            if msgobj.author == self.client.user:
                                if msgobj.content == message:
                                    if len(possiblemsgobj) < 1:
                                        h = f"{msgobj.guild.id}/{msgobj.channel.id}/{msgobj.id}"
                                        possiblemsgobj.append(f"https://discordapp.com/channels/{h}")

                        await ctx.author.send("Your message has been sent", delete_after=60)
                        await log.send(f"""{ctx.author} ({ctx.author.id}) sent the following here <{possiblemsgobj[0]}>
""", delete_after=86400)
                        await log.send(message, delete_after=86400)
                else:
                    await ctx.send("Sorry, but we couldn't find the channel you wanted us to send this too")

    @commands.command(aliases=['uwutranslator'])
    async def uwu(self, ctx, *, untranslated="No text"):
        semitranslated = untranslated.replace('l', 'w')
        translated = semitranslated.replace('r', 'w')
        await ctx.send(translated+' uwu')

    @commands.command()
    async def entryembed(self, ctx):
        embed = discord.Embed(
            title='Choose a role',
            description=''':regional_indicator_a:: option 1
:regional_indicator_b:: option 2
:regional_indicator_c:: option 3
:regional_indicator_d:: option 4''',
            colour=discord.Colour.green()
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def bandembed(self, ctx):
        embed = discord.Embed(
            title='Which band(s) are you in?',
            description=""":one:: concert band
    :two:: symphonic band
    :three:: marching band
    :four:: jazz band
    :five:: jazz ensemble""",
            colour=discord.Colour.green()
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Misc(client))
