import requests
import json
from datetime import datetime, timedelta
import locale
import os
import re
from helpers import updateContribution
from dotenv import load_dotenv
load_dotenv()

AM4_TOKEN = os.getenv("AM4_API_TOKEN")
locale.setlocale(locale.LC_ALL, 'en_US.utf8')


def contributionReq():
    response = requests.get(
        f'https://www.airline4.net/api/?access_token={AM4_TOKEN}&search=jet2%20alliance')
    if (response.status_code == 200):
        return response.text
    elif (response.status_code == 404):
        return 0


def getOne(args):
    now = datetime.now()
    members = json.loads(contributionReq())
    resetDate = datetime(2020, 3, 16)
    data = {
        "name": "",
        "days": "",
        'total': '',
        'avr': '',
        'flights': '',
        'fligthsAvr': '',
        'contriFligth': '',
        'share': '',
        'totalReq': members["status"]["requests_remaining"],
        'place': 0,
        'diffYesterday': 0,
        'yesterday': 0,
        'flightYesterday': 0,
        'flightDiff': 0,
    }

    companyName = ''
    if (len(args) == 1):
        companyName = args[0]
    if (len(args) > 1):
        companyName = f'{args[0]} {args[1]}'

    i = 0
    for x in members["members"]:
        i = i+1

        if (companyName.lower() in x["company"].lower()):
            delta = int((now - resetDate).days)
            delta2 = now - datetime.fromtimestamp(x['joined'])

            wks = updateContribution.downloadSheet()
            wks = wks.worksheet("newData")
            row = wks.find(x['company']).row
            index = f'E{row}'
            todayCont = wks.acell(index).value
            todayContValue = int(re.sub('[$,]+', '', todayCont))

            index = f'F{row}'
            todayFlight = wks.acell(index).value
            todayFlightValue = int(re.sub('[$,]+', '', todayFlight))

            index = f'N{row}'
            yesterdayCont = wks.acell(index).value
            yesterdayContValue = int(re.sub('[$,]+', '', yesterdayCont))

            index = f'P{row}'
            yesterdayFlight = wks.acell(index).value
            yesterdayFlightValue = int(re.sub(',', '', yesterdayFlight))

            if (int(delta2.days) < int(delta)):
                delta = delta2.days

            contriDay = round(
                x["contributed"] / delta, 2)
            fligthsDay = int(x["flights"] / delta)
            contriFligth = round(x['contributed']/x['flights'], 2)

            data["name"] = x["company"]
            data["days"] = delta
            data["total"] = f'$ {locale.format("%d", x["contributed"],grouping=True)}'
            data['avr'] = f'$ {locale.format("%d", contriDay, grouping=True)}'
            data['flights'] = locale.format("%d",  x["flights"], grouping=True)
            data['fligthsAvr'] = locale.format("%d", fligthsDay, grouping=True)
            data['contriFligth'] = f'$ {contriFligth}'
            data['share'] = f'$ {x["shareValue"]}'
            data['place'] = i
            data['diffYesterday'] = f'$ {locale.format("%d", x["contributed"]-todayContValue,grouping=True)}'
            data['yesterday'] = locale.format(
                "%d", yesterdayContValue, grouping=True)
            data['flightYesterday'] = locale.format(
                "%d", yesterdayFlightValue, grouping=True)
            data['flightDiff'] = f'{locale.format("%d", x["flights"]-yesterdayFlightValue,grouping=True)}'
    return data
