from discord.ext import tasks, commands
from discord import Embed
from helpers import getFuelData
import re


class FuelMessenger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.maxCo2Price = 140
        self.maxFuelPrice = 1000
        self.minFuelPrice = 500
        print("Fuel Messenger command initialized")

    @commands.Cog.listener()
    async def on_ready(self):
        self.sendFuel.start()
        print('We have logged in')

    def cog_unload(self):
        print("Unload Fuel Messenger command")

    @tasks.loop(seconds=1800)
    async def sendFuel(self):

        channel = self.client.get_channel(687252161222017151)
        price = {}
        price['fuelPrice'] = int(re.sub(
            '[,]+', '', getFuelData.getFuelPrice()))
        price['co2Price'] = int(re.sub(
            '[,]+', '', getFuelData.getC02Price()))

        await self.message(price, channel)

    async def message(self, price, channel):
        send = 0
        embed = Embed(title="Fuel & CO2 Price",
                      description='Prices of fuel at the moment', color=0xff0000)
        embed.set_thumbnail(
            url="https://image.flaticon.com/icons/png/512/172/172175.png")

        myid = '<@&699301333924052994>'
        if (price['fuelPrice'] <= self.maxFuelPrice):
            embed.add_field(name="Fuel Price",
                            value=f'{price["fuelPrice"]} $', inline=False)
            send = 1
            if (price['fuelPrice'] <= self.minFuelPrice):

                await channel.send('%s' % myid)

        if (price['co2Price'] <= self.maxCo2Price):
            embed.add_field(name="CO2 Price",
                            value=f'{price["co2Price"]} $', inline=False)
            send = 1

        if (send == 1):
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(FuelMessenger(client))
