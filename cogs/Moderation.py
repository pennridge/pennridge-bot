import discord
from discord.ext import commands
import typing

Grades = ['Freshman', 'Sophomore', 'Junior', 'Senior']
Subjects = ["Math", "English", "Social-studies", "Science", "Languages"]
    
Modrole = "Mod"


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked by {ctx.author.mention} for **{reason}**")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"{ctx.author.mention} gave {member.mention} the ban hammer for **{reason}**")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages got yote by {ctx.author.mention}")

    @commands.command()
    @commands.has_role(Modrole)
    async def say(self, ctx, receiver: typing.Union[discord.TextChannel, discord.Member], *, msg: str):
        for embed in ctx.message.attachments:
            msg += f" {embed.url}"
        await receiver.send(msg)


    @commands.command()
    @commands.has_role(Modrole)
    async def createcategories(self, ctx):
        studentrole = discord.utils.get(ctx.guild.roles, name="Student")
        see_all = discord.utils.get(ctx.guild.roles, name="See all")
        for i in Grades:
            graderole = discord.utils.get(ctx.guild.roles, name=i)
            await ctx.guild.create_category(i)
            Category = discord.utils.get(ctx.guild.categories, name=i)
            await Category.set_permissions(studentrole, read_messages=False,
                                           send_messages=False)
            await Category.set_permissions(see_all, read_messages=True)
            await Category.set_permissions(graderole, read_messages=True,
                                           send_messages=True)
            await ctx.guild.create_text_channel(f"{i}-General", category=Category)
            for i2 in Subjects:
                await ctx.guild.create_text_channel(i2, category=Category)
            print(f"{i} completed")
        await ctx.send('done')

    
def setup(client):
    client.add_cog(Mod(client))
