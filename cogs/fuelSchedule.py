from discord.ext import commands
from discord import Embed
import json
from helpers import fuelSchedule, isAdmin


class Fuel(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Joke command initialized")

    @commands.check(isAdmin.isAdmin)
    @commands.command(name="fuel", help='fuel', description='Fuel schedule')
    async def fuel(self, ctx, *args):
        fuel = await fuelSchedule.getInfo(args)
        embed = Embed()
        string = ""
        embed = Embed(title=f"Fuel Schedule Day {args[0]}",
                      color=0xff0000)
        embed.set_thumbnail(
            url="https://image.flaticon.com/icons/png/512/172/172175.png")
        for x in fuel:
            string = string + f"{x['schedule']} : {x['co2']}\n"

        embed.add_field(name="Co2 Schedule",
                        value=string, inline=True)

        embed.set_footer(
            text=f'Data updated live from our database;\nCreated by Phobo Inc')

        await ctx.send(embed=embed)

    # async def sendJoke(self, ctx, joke):
        # embed = Embed(title="Dad Joke",
        #               color=0xff0000)

        # embed.set_thumbnail(
        #     url="https://www.dictionary.com/e/wp-content/uploads/2018/06/dad-joke.jpg")
        # embed.add_field(name="Joke",
        #                 value=f'{joke}', inline=False)

        # embed.set_footer(
        #     text=f'Data updated live \nCreated by Phobo Inc')
        # await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fuel(client))
