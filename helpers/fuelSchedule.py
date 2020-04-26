import datetime as dt
import time
import re
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
import gspread


def downloadSheet():

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'fueldata.json', scope)

    gc = gspread.authorize(credentials)

    return gc.open("Airline Manager 4 Co2 and Fuel Table")


async def getInfo(args):
    fuelPriceMax = 600
    co2PriceMax = 125
    wks = downloadSheet()
    day = args[0]

    if (len(args) > 2):
        fuelPriceMax = int(args[1])
    if(len(args) > 2):
        co2PriceMax = int(args[2])

    co2Sheet = wks.worksheet("CO2")
    fuelSheet = wks.worksheet("New Fuel")

    scheduleTime = co2Sheet.col_values(1)
    co2List = co2Sheet.col_values(int(day) + 1)
    fuelList = fuelSheet.col_values(int(day) + 1)
    del fuelList[0:3]
    del co2List[0:3]
    del scheduleTime[0:3]
    table = []

    for x in range(len(scheduleTime)):
        fPrice = re.sub('[$,]+', '', fuelList[x])
        co2Price = re.sub('[$,]+', '', co2List[x])
        fPrice = int(0 if fPrice == '' else int(fPrice))
        cPrice = int(0 if co2Price == '' else int(co2Price))

        # if (fPrice == 0):
        #     gap.append(scheduleTime[x])

        data = {
            "fPrice": '\'High\'',
            "cPrice": '\'High\''
        }

        if (cPrice != 0 or fPrice != 0):
            if (cPrice != 0):
                if (cPrice < co2PriceMax):
                    data["cPrice"] = cPrice
            if (fPrice < fuelPriceMax):

                data["fPrice"] = fPrice
            if (data['cPrice'] != "\'High\'" or data['fPrice'] != "\'High\'"):
                if (len(scheduleTime[x]) < 5):
                    scheduleTime[x] = f'0{scheduleTime[x]}'

                if (len(str(data['fPrice'])) < 5):
                    data['fPrice'] = f' {str(data["fPrice"])}  '
                if (len(str(data['cPrice'])) < 5):
                    data['cPrice'] = f' {str(data["cPrice"])}'

                table.append(
                    {"schedule": scheduleTime[x], "co2": data["cPrice"], "fuel": data["fPrice"]})

                # table.add_row(
                #     [scheduleTime[x], data["fPrice"], data["cPrice"]])
    return table
    # print("\n\nTimeline in schedules are referring to UTC Game Time, the same as the Game")
    # print(
    #     f"Schedule for the day {day}, co2Price < {co2PriceMax}")
    # # print(
    # #     f"Schedule for the day {day}, fuelPrice < {fuelPriceMax}, co2Price < {co2PriceMax}")
    # print(table)
    # if(len(gap) > 2):
    #     print(
    #         f"\033[1;30;41m Note: \x1b[0m We dont have info beetwen {gap[0]} and {gap[len(gap)-1]} so judge for yourself")
