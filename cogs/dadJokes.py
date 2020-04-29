from discord.ext import commands
from discord import Embed
import json
from helpers import dadJoke


class Joke(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Joke command initialized")

    def cog_unload(self):
        print("Unload dadJoke command")

    @commands.command(name="joke", help='Dad Jokes for everyone', description='Call me and i will tell you the best Jokes')
    async def joke(self, ctx):
        joke = dadJoke.getJoke()
        joke = joke['joke']

        economy = self.client.get_cog('Contri')
        if economy is not None:

            value = await economy.getValue()

        await self.sendJoke(ctx, joke)

    async def sendJoke(self, ctx, joke):
        embed = Embed(title="Dad Joke",
                      color=0xff0000)

        embed.set_thumbnail(
            url="https://www.dictionary.com/e/wp-content/uploads/2018/06/dad-joke.jpg")
        embed.add_field(name="Joke",
                        value=f'{joke}', inline=False)

        embed.set_footer(
            text=f'Data updated live \nCreated by Phobo Inc')

        await ctx.send(embed=embed)
        print(f'{ctx.author} called the dad jokes')


def setup(client):
    client.add_cog(Joke(client))
