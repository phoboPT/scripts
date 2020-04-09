import discord
from discord.ext import commands
import requests
import json
from prettytable import PrettyTable
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_ALL, 'en_US')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="contri", help='Responds with a random quote from Brooklyn 99')
async def contri(ctx, *args):
    members = json.loads(contributionReq())
    table = getOne(members, args)

    user = bot.get_user(ctx.author.id)

    embed = discord.Embed(title="Contribution Status",
                          description=table["name"], color=0xff0000)
    embed.set_author(name=ctx.author,  icon_url=user.avatar_url)
    embed.set_thumbnail(
        url="https://image.flaticon.com/icons/png/512/172/172175.png")
    embed.add_field(name="Company name", value=table["name"], inline=False)
    embed.add_field(name="Days", value=table["days"], inline=True)
    embed.add_field(name="Total Contribution",
                    value=table["total"], inline=True)
    embed.add_field(name="Contribution/Day", value=table["avr"], inline=True)
    embed.add_field(name="Flights", value=table["flights"], inline=True)
    embed.add_field(name="Flights/Day", value=table["fligthsAvr"], inline=True)
    embed.add_field(name="Contribution/Flight",
                    value=table["contriFligth"], inline=True)
    embed.set_footer(text="Created by Phobo Inc")
    await ctx.message.channel.send(embed=embed)



def contributionReq():
    response = requests.get(
        'https://www.airline4.net/api/?access_token=klJLKFhweiuyOIsdbfW.ewrm8723LKjhdsQWtyudfnbLKUW&search=jet2%20alliance')
    if (response.status_code == 200):
        return response.text
    elif (response.status_code == 404):
        return 0


def calcTimestamps(members):
    now = datetime.now()
    table = PrettyTable()
    table.field_names = ["Name", "Days", 'Total Contribution',
                         'Contribution/Day', 'Fligths', 'Flights/Day', 'Contribution/Fligth']

    for x in members["members"]:

        delta = now-datetime.fromtimestamp(
            1584353085)
        delta2 = now - datetime.fromtimestamp(x['joined'])

        if (int(delta2.days) <= 24):
            delta = delta2

        # print(f' {x["company"]} {x["contributed"]/delta.days}')
        contriDay = round(
            x["contributed"] / delta.days, 2)
        fligthsDay = round(x["flights"] / delta.days, 2)
        contriFligth = round(x['contributed'] / x['flights'])

        table.add_row([x["company"], delta.days, x['contributed'],
                       contriDay, x["flights"], fligthsDay, contriFligth])
    return table


def getOne(members, args):
    now = datetime.now()
    table = PrettyTable()
    table.field_names = ["Name", "Days", 'Total Contribution',
                         'Avr.Contribution', 'Fligths', 'Flights/Day', 'Contribution/Fligth']

    data = {
        "name": "",
        "days": "",
        'total': '',
        'avr': '',
        'flights': '',
        'fligthsAvr': '',
        'contriFligth': ''
    }
    companyName = ''
    if (len(args) == 1):
        companyName = args[0]
    if (len(args) > 1):
        companyName = f'{args[0]} {args[1]}'

    for x in members["members"]:

        if (companyName.lower() in x["company"].lower()):

            delta = now-datetime.fromtimestamp(
                1584353085)
            delta2 = now - datetime.fromtimestamp(x['joined'])

            if (int(delta2.days) <= 24):
                delta = delta2

                # print(f' {x["company"]} {x["contributed"]/delta.days}')
            contriDay = round(
                x["contributed"] / delta.days, 2)
            fligthsDay = int(x["flights"] / delta.days)
            contriFligth = round(x['contributed']/x['flights'], 2)
            # table.add_row([x["company"], delta.days, x['contributed'],
            #                contriDay, x["flights"], fligthsDay, contriFligth])
            data["name"] = x["company"]
            data["days"] = delta.days
            data["total"] = f'$ {x["contributed"]}'
            data['avr'] = f'$ {locale.format("%d", contriDay, grouping=True)}'
            data['flights'] = x["flights"]
            data['fligthsAvr'] = fligthsDay
            data['contriFligth'] = f'$ {contriFligth}'
    return data


bot.run('NjkwMzQ2OTgwMzI0NjcxNjI3.Xo8AHA.e_Nt9owhCX35ScJj_xy-4HnD8w4')
