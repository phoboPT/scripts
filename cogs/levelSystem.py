from discord.ext import commands
import discord


class LevelSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Level System command initialized")


def setup(client):
    client.add_cog(LevelSystem(client))
