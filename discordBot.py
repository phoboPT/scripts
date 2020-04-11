import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure

import updateContribution
import contributionHelper


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="contri", help='Member Contribution for the alliance', usage='COMPANY_NAME', description='Im a Contribution helper, you tell me your company, i tell you your performance')
async def contri(ctx, *args):

    table = contributionHelper.getOne(args)

    user = bot.get_user(ctx.author.id)

    embed = discord.Embed(title="Contribution Status",
                          description=table["name"], color=0xff0000)
    embed.set_author(name=ctx.author,  icon_url=user.avatar_url)
    embed.set_thumbnail(
        url="https://image.flaticon.com/icons/png/512/172/172175.png")
    embed.add_field(name="Company name", value=table["name"], inline=False)
    embed.add_field(name="#", value=table["place"], inline=True)
    embed.add_field(name="Days", value=table["days"], inline=True)
    embed.add_field(name="Total Contribution",
                    value=table["total"], inline=True)
    embed.add_field(name="Contribution/Day", value=table["avr"], inline=True)
    embed.add_field(name="Flights", value=table["flights"], inline=True)
    embed.add_field(name="Flights/Day", value=table["fligthsAvr"], inline=True)
    embed.add_field(name="Contribution/Flight",
                    value=table["contriFligth"], inline=True)
    embed.add_field(name="Share",
                    value=table["share"], inline=True)
    embed.set_footer(
        text=f'Data updated live from the AM4 API; requests remaining: {table["totalReq"]}\nCreated by Phobo Inc')
    await ctx.message.channel.send(embed=embed)


@bot.command(name="update", help='Contribution Sheet updater', description='Im a Contribution updater, call me and i will update the sheet')
async def updateSheet(ctx, *args):
    print(ctx.author.id)

    if(ctx.author.id == 343714644147568650 or ctx.author.id == 686986610142740521 or ctx.author.id == 558418745463406594 or ctx.author.id == 619574286356578336):
        await ctx.message.channel.send("Updating Sheet")
        await updateContribution.saveSheet(ctx)
        await ctx.message.channel.send("Sheet Updated")
    else:
        await ctx.message.channel.send("You don't have permissions to use this command")


bot.run('NjkwMzQ2OTgwMzI0NjcxNjI3.Xo8AHA.e_Nt9owhCX35ScJj_xy-4HnD8w4')
