import discord
from discord.ext import commands


def isAdmin(ctx):
    return ctx.author.id == 343714644147568650 or ctx.author.id == 686986610142740521 or ctx.author.id == 558418745463406594 or ctx.author.id == 619574286356578336 or ctx.author.id == 661953774734016512


class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Purge command initialized")

    @commands.command(name="purge", help='Purge tue given amount of messages', description='I\'m a board cleaner')
    @commands.check(isAdmin)
    async def purge(self, ctx, ammount):
        await ctx.message.channel.purge(limit=int(ammount))
        print(f"{ctx.author} calleg purge and purged {ammount} messages")


def setup(client):
    client.add_cog(Purge(client))
