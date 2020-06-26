import requests
import json
from datetime import datetime, timedelta
import locale
import os
import re
#import updateContribution
from helpers import updateContribution
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from matplotlib import style
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


async def getOne(args):
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

    if (len(args) == 1):
        companyName = args[0]
    if (len(args) > 1):
        companyName = f'{args[0]} {args[1]}'

    companyName = ''
    i = 0
    for x in members["members"]:
        i = i+1
        if (companyName.lower() in x["company"].lower()):
            delta = int((now - resetDate).days)
            delta2 = now - datetime.fromtimestamp(x['joined'])

            wks = updateContribution.downloadSheet()
            wks = wks.worksheet("newData")
            row = wks.find(x['company']).row

            # Graph
            # day1
            index = f'R{row}'
            day1 = wks.acell(index).value
            # day2
            index = f'S{row}'
            day2 = wks.acell(index).value
            # day3
            index = f'T{row}'
            day3 = wks.acell(index).value
            # day4
            index = f'U{row}'
            day4 = wks.acell(index).value
            # day5
            index = f'V{row}'
            day5 = wks.acell(index).value
            # day6
            index = f'W{row}'
            day6 = wks.acell(index).value
            # day7
            index = f'X{row}'
            day7 = wks.acell(index).value
            # yesterday
            index = f'N{row}'
            day8 = wks.acell(index).value

            day1 = int(re.sub('[,]+', '', day1))
            day2 = int(re.sub('[,]+', '', day2))
            day3 = int(re.sub('[,]+', '', day3))
            day4 = int(re.sub('[,]+', '', day4))
            day5 = int(re.sub('[,]+', '', day5))
            day6 = int(re.sub('[,]+', '', day6))
            day7 = int(re.sub('[,]+', '', day7))
            day8 = int(re.sub('[$,]+', '', day8))

            total = day2+day3+day4+day5+day6+day7+day8
            print(day8)
            plt.clf()

            days = {"1": day1, "2": day2, "3": day3,
                    "4": day4, "5": day5, "6": day6, "7": day7, "Yesterday": day8}

            names = list(days.keys())
            values = list(days.values())
            yAxys = sorted(values)

            last = yAxys[7] + 2000
            yAxys[0] = f'{locale.format_string("%d", yAxys[0],grouping=True)}'
            yAxys[1] = f'{locale.format_string("%d", yAxys[1],grouping=True)}'
            yAxys[2] = f'{locale.format_string("%d", yAxys[2],grouping=True)}'
            yAxys[3] = f'{locale.format_string("%d", yAxys[3],grouping=True)}'
            yAxys[4] = f'{locale.format_string("%d", yAxys[4],grouping=True)}'
            yAxys[5] = f'{locale.format_string("%d", yAxys[5],grouping=True)}'
            yAxys[6] = f'{locale.format_string("%d", yAxys[6],grouping=True)}'
            yAxys[7] = f'{locale.format_string("%d", yAxys[7],grouping=True)}'
            yAxys.insert(
                8, f'{locale.format_string("%d", last,grouping=True)}')

            values[0] = f'{locale.format_string("%d", values[0],grouping=True)}'
            values[1] = f'{locale.format_string("%d", values[1],grouping=True)}'
            values[2] = f'{locale.format_string("%d", values[2],grouping=True)}'
            values[3] = f'{locale.format_string("%d", values[3],grouping=True)}'
            values[4] = f'{locale.format_string("%d", values[4],grouping=True)}'
            values[5] = f'{locale.format_string("%d", values[5],grouping=True)}'
            values[6] = f'{locale.format_string("%d", values[6],grouping=True)}'
            values[7] = f'{locale.format_string("%d", values[7],grouping=True)}'

            fig = plt.figure()

            plt.style.use('dark_background')
            ax = plt.axes()

            ax.plot([0, 0, 0, 0, 0, 0, 0, 0, 0], yAxys, color='black')
            # zip joins x and y co  ordinates in pairs
            for y, z in zip(names, values):
                label = z
                plt.annotate(label,  # this is the text
                             (y, z),  # this is the point to label
                             textcoords="offset points",  # how to position the text
                             # distance from text to points (x,y)
                             xytext=(0, 10),
                             ha='center')  # horizontal alignment can be left, right or center

            plt.plot(names, values, 'o-', label='curPerform', color='r')
            # plt.show()
            plt.savefig("online.png")
            plt.close(fig=fig)

            index = f'P{row}'
            yesterdayFlight = wks.acell(index).value
            yesterdayFlightValue = int(re.sub(',', '', yesterdayFlight))
            index = f'E{row}'
            todayCont = wks.acell(index).value
            todayContValue = int(re.sub('[$,]+', '', todayCont))

            index = f'F{row}'
            todayFlight = wks.acell(index).value
            todayFlightValue = int(re.sub('[$,]+', '', todayFlight))

            index = f'N{row}'
            yesterdayCont = wks.acell(index).value
            yesterdayContValue = int(re.sub('[$,]+', '', yesterdayCont))

            if (int(delta2.days) < int(delta)):
                delta = delta2.days

            contriDay = round(x["contributed"] / delta, 2)
            fligthsDay = int(x["flights"] / delta)
            contriFligth = round(x['contributed']/x['flights'], 2)
            data["name"] = x["company"]
            data["days"] = delta
            data["total"] = f'$ {locale.format_string("%d", x["contributed"],grouping=True)}'
            data['avr'] = f'$ {locale.format_string("%d", contriDay, grouping=True)}'
            data['flights'] = locale.format_string(
                "%d",  x["flights"], grouping=True)
            data['fligthsAvr'] = locale.format_string(
                "%d", fligthsDay, grouping=True)
            data['contriFligth'] = f'$ {contriFligth}'
            data['share'] = f'$ {x["shareValue"]}'
            data['place'] = f'$ {locale.format_string("%d", total, grouping=True)}'
            data['diffYesterday'] = f'$ {locale.format_string("%d", x["contributed"]-todayContValue,grouping=True)}'
            data['yesterday'] = locale.format_string(
                "%d", yesterdayContValue, grouping=True)
            data['flightYesterday'] = locale.format_string(
                "%d", yesterdayFlightValue, grouping=True)
            data['flightDiff'] = f'{locale.format_string("%d", x["flights"]-todayFlightValue,grouping=True)}'
    return data
