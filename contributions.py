import discord
from discord.ext import commands
import requests
import json
from prettytable import PrettyTable
from datetime import datetime, timedelta
import locale


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

        contriDay = round(
            x["contributed"] / delta.days, 2)
        if (contriDay < 7000):
            contriDay = f'\033[1;31;40m {contriDay}  \x1b[0m'
        fligthsDay = round(x["flights"] / delta.days, 2)
        contriFligth = round(x['contributed'] / x['flights'])

        table.add_row([x["company"], delta.days, x['contributed'],
                       contriDay, x["flights"], fligthsDay, contriFligth])
    return table


members = json.loads(contributionReq())
table = calcTimestamps(members)
print(table)
