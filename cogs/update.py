import discord
from discord.ext import commands, tasks
from helpers import updateContribution
from helpers import isAdmin
from datetime import datetime


class Update(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.executed = False
        print("Update command initialized")

    @commands.Cog.listener()
    async def on_ready(self):
        self.update.start()
        print('We have logged in')

    def cog_unload(self):
        print("Unload update command")

    @commands.command(name="update", help='Contribution Sheet updater', description='Im a Contribution updater, call me and i will update the sheet')
    @commands.check(isAdmin.isAdmin)
    async def updateSheet(self, ctx):
        channel = self.client.get_channel(725038386208833576)
        print(f' called the update')
        await ctx.send(f"Updating Sheet ")
        await updateContribution.saveSheet(ctx, channel)
        await ctx.send("Sheet Updated")

    @tasks.loop(seconds=3600)
    async def update(self):

        channel = self.client.get_channel(697768447882559548)
        channel2 = self.client.get_channel(725038386208833576)
        # await channel.send("Updating Sheet")
        # await updateContribution.saveSheet(channel, channel2)
        # await channel.send("Sheet Updated")


def setup(client):
    client.add_cog(Update(client))
