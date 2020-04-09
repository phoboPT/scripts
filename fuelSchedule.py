import datetime as dt
import time
import re
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
import gspread
import sys
from prettytable import PrettyTable


def downloadSheet():

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'fueldata.json', scope)

    gc = gspread.authorize(credentials)

    return gc.open("Airline Manager 4 Co2 and Fuel Table")


def getInfo(args):
    fuelPriceMax = 600
    co2PriceMax = 125
    wks = downloadSheet()
    day = args[1]

    if (len(args) > 2):
        fuelPriceMax = int(args[2])
    if(len(args) > 3):
        co2PriceMax = int(args[3])

    co2Sheet = wks.worksheet("CO2")
    fuelSheet = wks.worksheet("New Fuel")

    scheduleTime = fuelSheet.col_values(1)
    co2List = co2Sheet.col_values(int(day) + 1)
    fuelList = fuelSheet.col_values(int(day) + 1)
    del fuelList[0:3]
    del co2List[0:3]
    del scheduleTime[0:3]

    table = PrettyTable()

    table.field_names = ["Time", "Fuel", 'CO2']
    gap = []
    for x in range(len(scheduleTime)):
        fPrice = re.sub('[$,]+', '', fuelList[x])
        co2Price = re.sub('[$,]+', '', co2List[x])
        fPrice = int(0 if fPrice == '' else int(fPrice))
        cPrice = int(0 if co2Price == '' else int(co2Price))

        if (fPrice == 0):
            gap.append(scheduleTime[x])

        data = {
            "fPrice": '\033[1;31;40m High  \x1b[0m',
            "cPrice": '\033[1;31;40m High  \x1b[0m'
        }

        if (cPrice != 0 or fPrice != 0):
            if (cPrice < co2PriceMax):
                data["cPrice"] = cPrice
            if (fPrice < fuelPriceMax):
                data["fPrice"] = fPrice
            if (data['cPrice'] != "\033[1;31;40m High  \x1b[0m" or data['fPrice'] != '\033[1;31;40m High  \x1b[0m'):

                table.add_row(
                    [scheduleTime[x], data["fPrice"], data["cPrice"]])

    print("\n\nTimeline in schedules are referring to UTC Game Time, the same as the Game")
    print(
        f"Schedule for the day {day}, fuelPrice < {fuelPriceMax}, co2Price < {co2PriceMax}")
    print(table)
    if(len(gap) > 2):
        print(
            f"\033[1;30;41m Note: \x1b[0m We dont have info beetwen {gap[0]} and {gap[len(gap)-1]} so judge for yourself")


getInfo(sys.argv)
