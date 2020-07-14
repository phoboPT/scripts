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
        print("hi")
        # self.sendFuel.start()

    def cog_unload(self):
        print("Unload Fuel Messenger command")

    @tasks.loop(seconds=1800)
    async def sendFuel(self):

        channel = self.client.get_channel(687252161222017151)
        # channel = self.client.get_channel(697768447882559548)
        price = {}
        price['fuelPrice'] = int(re.sub(
            '[,]+', '', getFuelData.getFuelPrice()))
        price['co2Price'] = int(re.sub(
            '[,]+', '', getFuelData.getC02Price()))

        await self.message(price, channel)

    async def message(self, price, channel):
        send = 0

        myid = '<@&699301333924052994>'
        # myid = '<@&698179530711629854>'
        # price['fuelPrice'] = 400
        # price['co2Price'] = 120
        string = f"{myid}"

        if (price['fuelPrice'] <= self.maxFuelPrice):
            string = string+f'Fuel Price {price["fuelPrice"]}$'
            send = 1

        if (price['co2Price'] <= self.maxCo2Price):
            string = string+f' CO2 Price {price["co2Price"]}$'
            send = 1

        if (send == 1):
            await channel.send(string)


def setup(client):
    client.add_cog(FuelMessenger(client))
