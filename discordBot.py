import discord
from discord.ext import commands
import updateContribution
import contributionHelper

bot = commands.Bot(command_prefix='!')


def isAdmin(ctx):
    return ctx.author.id == 343714644147568650 or ctx.author.id == 686986610142740521 or ctx.author.id == 558418745463406594 or ctx.author.id == 619574286356578336 or ctx.author.id == 661953774734016512


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        ctx.send("Command not found, use !help")

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing some arguments")


@bot.command(name="contri", help='Member Contribution for the alliance', usage='COMPANY_NAME', description='Im a Contribution helper, you tell me your company, i tell you your performance')
async def contri(ctx, *args):
    if (len(args) == 0):
        await ctx.send("You are missing some arguments, use !contri <Name>")
    else:
        table = contributionHelper.getOne(args)

        user = bot.get_user(ctx.author.id)

        embed = discord.Embed(title="Contribution Status",
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
        embed.add_field(name="Contribution/Day",
                        value=table["avr"], inline=True)
        embed.add_field(name="Flights", value=table["flights"], inline=True)
        embed.add_field(name="Flights/Day",
                        value=table["fligthsAvr"], inline=True)
        embed.add_field(name="Contribution/Flight",
                        value=table["contriFligth"], inline=True)
        embed.add_field(name="Share",
                        value=table["share"], inline=True)
        embed.set_footer(
            text=f'Data updated live from the AM4 API; requests remaining: {table["totalReq"]}\nCreated by Phobo Inc')
        await ctx.message.channel.send(embed=embed)
    print(f'{ctx.author} called the contribution helper')


@contri.error
async def contriError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing some arguments")


@bot.command(name="update", help='Contribution Sheet updater', description='Im a Contribution updater, call me and i will update the sheet')
@commands.check(isAdmin)
async def updateSheet(ctx, *args):
    print(f'{ctx.author} called the update')
    await ctx.message.channel.send("Updating Sheet")
    await updateContribution.saveSheet(ctx)
    await ctx.message.channel.send("Sheet Updated")


@bot.command(name="purge", help='Purge tue given amount of messages', description='I\'m a board cleaner')
@commands.check(isAdmin)
async def purge(ctx, *args):
    await ctx.message.channel.purge(limit=int(args[0]))
    print(f"Purged {args[0]}")


bot.run('NjkwMzQ2OTgwMzI0NjcxNjI3.Xo8AHA.e_Nt9owhCX35ScJj_xy-4HnD8w4')
