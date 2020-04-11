
import requests
import json
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


def contributionReq():
    response = requests.get(
        'https://www.airline4.net/api/?access_token=klJLKFhweiuyOIsdbfW.ewrm8723LKjhdsQWtyudfnbLKUW&search=jet2%20alliance')
    if (response.status_code == 200):
        return response.text
    elif (response.status_code == 404):
        return 0


def getOne(args):
    now = datetime.now()
    members = json.loads(contributionReq())
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
        'place': 0
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
            data['share'] = f'$ {x["shareValue"]}'
            data['place'] = i
    return data
