import discord
from discord.ext import commands
from helpers import isAdmin


class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Purge command initialized")

    def cog_unload(self):
        print("Unload purge command")

    @commands.command(name="purge", help='Purge tue given amount of messages', description='I\'m a board cleaner')
    @commands.check(isAdmin.isAdmin)
    async def purge(self, ctx, ammount):
        await ctx.message.channel.purge(limit=int(ammount))
        print(f"{ctx.author} calleg purge and purged {ammount} messages")


def setup(client):
    client.add_cog(Purge(client))
