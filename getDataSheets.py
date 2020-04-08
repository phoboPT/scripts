
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime as dt
import gspread


def downloadSheet():

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'fueldata.json', scope)

    gc = gspread.authorize(credentials)

    return gc.open("Airline Manager 4 Co2 and Fuel Table")


def saveSheet():
    today = dt.datetime.now()

    date = int(today.strftime("%d"))
    # adjustedTime = today-dt.timedelta(minutes=60)
    hour = today.strftime("%H")
    minutes = today.strftime("%M")
    index = 0
    if (int(minutes) > 30):
        index = (int(hour)*2)+3
    else:
        index = (int(hour)*2)+2

    print(hour, index)

    wks = downloadSheet()
    wks = wks.worksheet("CO2")

    index = 'E'+str(index)
    wks.updateSheet(index, 112)


if __name__ == '__main__':

    updateSheet()
