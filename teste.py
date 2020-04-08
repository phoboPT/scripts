import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'fueldata.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("Airline Manager 4 Co2 and Fuel Table").sheet1
wks.update('D37', 112)
