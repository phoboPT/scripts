from discord.ext import commands
import discord
from helpers import isAdmin
from helpers import contributionHelper


class Contri(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("ContriAll command initialized")

    def cog_unload(self):
        print("Unload contri command")

    @commands.command(name="contriall", help='Member Contribution for the alliance', usage='COMPANY_NAME', description='Im a Contribution helper, you tell me your company, i tell you your performance')
    @commands.check(isAdmin.isAdmin)
    async def contri(self, ctx, *args):
        text = await contributionHelper.getAll()

        string = "```ml\nName          Days Total      7Days    Today     Yesterday\n"
        string = string + text["0"]+"```"
        embed = discord.Embed(title=f"Contribution All",
                              color=0xff0000)
        embed.add_field(name="ALL MEMBERS",
                        value=string, inline=True)
        embed.set_footer(
            text=f'Data updated live from the AM4 API;\nCreated by Phobo Inc')
        await ctx.send(embed=embed)

        string = "```ml\nName          Days Total      7Days    Today     Yesterday\n"
        string = string + text["1"]+"```"
        embed = discord.Embed(title=f"Contribution All",
                              color=0xff0000)
        embed.add_field(name="ALL MEMBERS",
                        value=string, inline=True)
        embed.set_footer(
            text=f'Data updated live from the AM4 API;\nCreated by Phobo Inc')
        await ctx.send(embed=embed)

        string = "```ml\nName          Days Total      7Days    Today     Yesterday\n"
        string = string + text["2"]+"```"
        embed = discord.Embed(title=f"Contribution All",
                              color=0xff0000)
        embed.add_field(name="ALL MEMBERS",
                        value=string, inline=True)
        embed.set_footer(
            text=f'Data updated live from the AM4 API;\nCreated by Phobo Inc')
        await ctx.send(embed=embed)

        string = "```ml\nName          Days Total      7Days    Today     Yesterday\n"
        string = string + text["3"]+"```"
        embed = discord.Embed(title=f"Contribution All",
                              color=0xff0000)
        embed.add_field(name="ALL MEMBERS",
                        value=string, inline=True)
        embed.set_footer(
            text=f'Data updated live from the AM4 API;\nCreated by Phobo Inc')
        await ctx.send(embed=embed)

        string = "```ml\nName          Days Total      7Days    Today     Yesterday\n"
        string = string + text["4"]+"```"

        embed = discord.Embed(title=f"Contribution All",
                              color=0xff0000)
        embed.add_field(name="ALL MEMBERS",
                        value=string, inline=True)
        embed.set_footer(
            text=f'Data updated live from the AM4 API;\nCreated by Phobo Inc')
        await ctx.send(embed=embed)

        string = "```ml\nName          Days Total      7Days    Today     Yesterday\n"
        string = string + text["5"]+"```"
        embed = discord.Embed(title=f"Contribution All",
                              color=0xff0000)
        embed.add_field(name="ALL MEMBERS",
                        value=string, inline=True)
        embed.set_footer(
            text=f'Data updated live from the AM4 API;\nCreated by Phobo Inc')
        await ctx.send(embed=embed)

        print(f'{ctx.author} called the contribution all')


def setup(client):
    client.add_cog(Contri(client))
