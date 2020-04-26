from discord.ext import commands
from discord import Embed
from helpers import contributionHelper


class Contri(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Contri command initialized")

    @commands.command(name="contri", help='Member Contribution for the alliance', usage='COMPANY_NAME', description='Im a Contribution helper, you tell me your company, i tell you your performance')
    async def contri(self, ctx, *args):
        print(ctx.channel.id)
        if (len(args) == 0):
            await ctx.send("You are missing some arguments, use !contri <Name>")
        else:
            table = contributionHelper.getOne(args)
            print(table)
            user = self.client.get_user(ctx.author.id)
            embed = Embed(title="Contribution Status",
                          description=table["name"], color=0xff0000)
            embed.set_author(name=ctx.author,  icon_url=user.avatar_url)
            embed.set_thumbnail(
                url="https://image.flaticon.com/icons/png/512/172/172175.png")
            embed.add_field(name="Company name",
                            value=table["name"], inline=False)
            embed.add_field(name="#", value=table["place"], inline=True)
            embed.add_field(name="Days", value=table["days"], inline=True)
            embed.add_field(name="Total Contribution",
                            value=table["total"], inline=True)
            embed.add_field(name="Contribution done today",
                            value=table["diffYesterday"], inline=True)
            embed.add_field(name="Contribution/Day",
                            value=table["avr"], inline=True)

            embed.add_field(
                name="Flights", value=table["flights"], inline=True)
            embed.add_field(name="Flights/Day",
                            value=table["fligthsAvr"], inline=True)

            embed.add_field(name="Contribution/Flight",
                            value=table["contriFligth"], inline=True)
            embed.add_field(name="Share",
                            value=table["share"], inline=True)
            embed.set_footer(
                text=f'Data updated live from the AM4 API; requests remaining: {table["totalReq"]}\nCreated by Phobo Inc')
            await ctx.send(embed=embed)
        print(f'{ctx.author} called the contribution helper')

    async def getValue(self):
        print("hi")
        return "hello"


def setup(client):
    client.add_cog(Contri(client))
