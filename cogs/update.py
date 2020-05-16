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
        print(f' called the update')
        await ctx.send("Updating Sheet")
        await updateContribution.saveSheet(ctx)
        await ctx.send("Sheet Updated")

    @tasks.loop(seconds=300)
    async def update(self):

        now = datetime.now()
        hour = now.strftime("%H")

        if (int(hour) == 1 and self.executed == False):
            channel = self.client.get_channel(697768447882559548)
            await channel.send("Updating Sheet")
            await updateContribution.saveSheet(ctx)
            await channel.send("Sheet Updated")
            self.executed = True
        if (int(hour) != 1):
            self.executed = False


def setup(client):
    client.add_cog(Update(client))
