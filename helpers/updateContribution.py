import requests
from bs4 import BeautifulSoup
import time
import re
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import gspread
import json
import locale
import os
from dotenv import load_dotenv
load_dotenv()


AM4_TOKEN = os.getenv("AM4_API_TOKEN")

cell = {
    0: 'D',
    1: "E",
    2: "F",
    3: "G",
    4: "H",
    5: "I",
    6: "J",
    7: 'M',
    8: 'O'

}


def downloadSheet():

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'fueldata.json', scope)

    gc = gspread.authorize(credentials)

    return gc.open("Jet 2 Alliance Members Data")


def calcContri():
    now = datetime.now()
    allData = []
    members = json.loads(getContributions())
    resetDate = datetime(2020, 3, 16)

    for x in members["members"]:
        data = {
            "name": "",
            "days": "",
            'total': '',
            'avr': '',
            'flights': '',
            'fligthsAvr': '',
            'contriFligth': '',
        }

        delta = int((now - resetDate).days)

        delta2 = now - datetime.fromtimestamp(x['joined'])

        if (int(delta2.days) < int(delta)):
            delta = delta2.days
        contriDay = round(
            x["contributed"] / delta if delta != 0 else 1, 2)
        fligthsDay = int(x["flights"] / delta if delta != 0 else 1)
        contriFligth = round(x['contributed']/x['flights'], 2)

        data["name"] = x["company"]
        data["days"] = delta
        data["total"] = x["contributed"]
        data['avr'] = contriDay
        data['flights'] = x["flights"]
        data['fligthsAvr'] = fligthsDay
        data['contriFligth'] = contriFligth
        data['flight'] = contriFligth

        allData.append(data)
    return allData


async def saveSheet(ctx):
    wks = downloadSheet()
    wks = wks.worksheet("newData")
    data = calcContri()

    row = ''
    for player in data:
        await ctx.send(f'updating {player["name"]}')

        row = wks.find(player['name']).row
        index = f'{cell[1]}{row}'
        totalContri = wks.acell(index).value
        index = f'{cell[7]}{row}'
        wks.update_acell(index, totalContri)
        index = f'{cell[2]}{row}'
        totalFlights = wks.acell(index).value
        index = f'{cell[8]}{row}'
        wks.update_acell(index, totalFlights)

        index = f'{cell[0]}{row}'
        wks.update_acell(index, player["days"])
        index = f'{cell[1]}{row}'
        wks.update_acell(index, player["total"])
        index = f'{cell[2]}{row}'
        wks.update_acell(index, player["flights"])
        index = f'{cell[3]}{row}'
        wks.update_acell(index, player["avr"])
        index = f'{cell[4]}{row}'
        wks.update_acell(index, player["fligthsAvr"])
        index = f'{cell[5]}{row}'
        wks.update_acell(index, player["contriFligth"])

        time.sleep(10)


def getContributions():
    response = requests.get(
        f'https://www.airline4.net/api/?access_token={AM4_TOKEN}&search=jet2%20alliance')
    if (response.status_code == 200):
        return response.text
    elif (response.status_code == 404):
        return 0
