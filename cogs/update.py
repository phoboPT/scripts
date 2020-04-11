import discord
from discord.ext import commands
from helpers import updateContribution


def isAdmin(ctx):
    return ctx.author.id == 343714644147568650 or ctx.author.id == 686986610142740521 or ctx.author.id == 558418745463406594 or ctx.author.id == 619574286356578336 or ctx.author.id == 661953774734016512


class Update(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Update command initialized")

    @commands.command(name="update", help='Contribution Sheet updater', description='Im a Contribution updater, call me and i will update the sheet')
    @commands.check(isAdmin)
    async def updateSheet(self, ctx):
        print(f'{ctx.author} called the update')
        await ctx.send("Updating Sheet")
        await updateContribution.saveSheet(ctx)
        await ctx.send("Sheet Updated")


def setup(client):
    client.add_cog(Update(client))
