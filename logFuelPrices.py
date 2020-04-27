import requests
from bs4 import BeautifulSoup
import datetime as dt
import time
import re
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
import gspread
from dotenv import load_dotenv
import os
load_dotenv()
AM4_SCRAPPING_COOKIE = os.getenv("AM4_SCRAPPING_COOKIE")

dayToCell = {
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z",
    26: "AA",
    27: "AB",
    28: "AC",
    29: "AD",
    30: "AE",
    31: "AF"
}


def getFuelPrice():
    fuelHTML = requests.get(
        'https://www.airline4.net/fuel.php?fbSig=false&_=1584038619891',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie':  AM4_SCRAPPING_COOKIE},
    )

    if fuelHTML.status_code == 200:
        fuelInfo = BeautifulSoup(fuelHTML.text, 'html.parser')
    elif fuelHTML.status_code == 404:
        print('Not Found id=144424')
    return fuelInfo.find("span", id="sumCost").text


def getC02Price():
    co2HTML = requests.get(
        'https://www.airline4.net/co2.php?fbSig=false&_=1584038619905',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie':  AM4_SCRAPPING_COOKIE},
    )

    if co2HTML.status_code == 200:
        co2HTML = BeautifulSoup(co2HTML.text, 'html.parser')
    elif co2HTML.status_code == 404:
        print('Not Found id=144424')
    return co2HTML.find("span", id="sumCost").text


def downloadSheet():

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'fueldata.json', scope)

    gc = gspread.authorize(credentials)

    return gc.open("Airline Manager 4 Co2 and Fuel Table Phobo")


def saveSheet(fuelPrice, co2Price, today):

    date = int(today.strftime("%d"))

    hour = today-dt.timedelta(minutes=60)

    hour = int(hour.strftime("%H"))
    minutes = int(today.strftime("%M"))

    if (int(minutes) > 30):
        index = (hour*2)+5
    else:
        index = (hour * 2) + 4

    wks = downloadSheet()

    co2Sheet = wks.worksheet("CO2")
    fuelSheet = wks.worksheet("New Fuel")
    oldFuelSheet = wks.worksheet("OldFuel Check")
    oldCo2Sheet = wks.worksheet("OldCO2 Check")

    if (hour == 23):
        index = dayToCell[date - 1] + str(index)
    else:
        index = dayToCell[date] + str(index)

    oldFuelPrice = fuelSheet.acell(index).value or 0
    oldCo2Price = co2Sheet.acell(index).value or 0

    print(
        f"Fuel updated cell {index} with {fuelPrice}")
    fuelSheet.update_acell(index, fuelPrice)
    oldFuelSheet.update_acell(index, oldFuelPrice)
    print(f"CO2 updated cell {index} with {co2Price} old price {oldCo2Price}")
    oldCo2Sheet.update_acell(index, oldCo2Price)
    co2Sheet.update_acell(index, co2Price)
    if (oldFuelPrice != fuelPrice):
        print(
            f"Old fuel price is different, old price has {oldFuelPrice} new price is {fuelPrice}")
    if (oldCo2Price != co2Price):
        print(
            f"Old co2 price is different, old price has {oldCo2Price} new price is {co2Price}")


def getPrices():
    today = dt.datetime.now()
    fuelPrice = getFuelPrice()
    co2Price = getC02Price()
    date = today.strftime("%d")
    hour = today-dt.timedelta(minutes=60)
    hour = hour.strftime("%H:%M")

    f = open("priceLog.txt", "a")
    f.write(f"{date} {hour} {fuelPrice} {co2Price}\n")
    f.close

    saveSheet(fuelPrice, co2Price, today)
    print(f"done {date} {hour} {fuelPrice} {co2Price}")


while True:
    timeSleep = 1800
    try:
        getPrices()
    except:
        timeSleep = 10
        print("something went wrong")

    time.sleep(timeSleep)
