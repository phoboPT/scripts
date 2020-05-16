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

        myid = '<@&699301333924052994>'
        string = ""
        if (price['fuelPrice'] <= self.maxFuelPrice):
            string = f'Fuel Price {price["fuelPrice"]} $'
            send = 1
            if (price['fuelPrice'] <= self.minFuelPrice):
                print("teste")
                # await channel.send('%s' % myid)

        if (price['co2Price'] <= self.maxCo2Price):
            string = string+f'CO2 Price {price["co2Price"]} $'
            send = 1

        if (send == 1):
            embed = Embed(title=string)
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(FuelMessenger(client))
