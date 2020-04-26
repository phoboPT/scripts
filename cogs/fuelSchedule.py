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
        string = "```ml\n Time   Fuel    CO2\n"
        embed = Embed(title=f"Fuel Schedule Day {args[0]}",
                      color=0xff0000)

        for x in fuel:
            string = string + \
                f"{x['schedule']} : {x['fuel']} : {x['co2']}\n"

        string = string+"```"
        embed.add_field(name="Fuel Schedule",
                        value=string, inline=True)
        embed.set_footer(
            text=f'Data updated live from our database;\nCreated by Phobo Inc')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fuel(client))
