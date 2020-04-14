import re
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

aircraftIds = [
    1085744,
    1085889,
    1085955,
    1104502,
    1124155,
    1130979,
    1142088,
    1154454,
    1158998,
    1169288,
    1170820,
    1174794,
    1175903,
    1184480,
    1184481,
    1185406,
    1190897,
    1190898,
    1196609,
    1196611,
    1203961,
    1208602,
    1208603,
    1208604,
    1230052,
    1243055,
    1256728,
    1265923,
    1278888,
    1291675,
    1297563,
    1309222,
    1309417,
    1309431,
    1309432,
    1309433,
    1309511,
    1309512,
    1309513,
    1309514,
    1309542,
    1309543,
    1309544,
    1309545,
    1309551,
    1309552,
    1309553,
    1309554,
    1317841,
    1327254,
    1332036,
    1332051,
    1334644,
    1336963,
    1344344,
    1344378,
    1348377,
    1356090,
    1381157,
    1382319,
    1382351,
    1382387,
    1401875,
    1436266,
    1470921,
    1488988,
    1519604,
    1536528,
    1564262,
    1585240,
    1632485,
    1683208,
    1720507,
    1777005,
    1890708,
    1912436,
    2030163,
    2055339,
    2123085,
    2168546,
    2200067,
    2238988,
    2301294,
    2336284,
    2382014,
    2420782,
    2452833,
    2494875,
    2543137,
    2576723,
    2605412,
    2628479,
    2657889,
    2682175,
    2714235,
    2740171,
    2770196,
    2799544,
    2827380,
    2842585,
    2860138,
    2907058,
    2952139,
    2981816,
    3015347,
    3033918,
    3054532,
    3081457,
    3111030,
    3148269,
    3188214,
    3216999
]
info = []

for x in aircraftIds:
    response = requests.get(
        'https://am4.pagespeedster.com/am4/fleet_details.php?id=' +
        str(x) + '&fbSig=false',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )
    if response.status_code == 200:
        info.append(BeautifulSoup(response.text, 'html.parser'))
    elif response.status_code == 404:
        print('Not Found id=' + x)

aircraftDetails = []
# get info from aircraft
for x in aircraftIds:
    response = requests.get(
        'https://am4.pagespeedster.com/am4/flight_info.php?id=' +
        str(x) + '&fbSig=false',

        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )
    if response.status_code == 200:
        aircraftDetails.append(BeautifulSoup(response.text, 'html.parser'))
    elif response.status_code == 404:
        print('Not Found id=' + x)

acDetails = []
origin = []
destination = []
departTime = []
arriveTime = []
routeDistance = []
fuel = []
paxOnBoard = []
aircraftName = []

for ac in aircraftDetails:
    try:
        routeTemp = ac.findAll(class_='row p-2')
        table = ac.findAll('table')
        routeDistance.append(table[0].select('td:nth-of-type(2)')[0].text)
        fuel.append(routeTemp[4].find("span", id="flightInfoFuel").text)
        origin.append(routeTemp[1].select('div:nth-of-type(1)')[0].text)
        destination.append(routeTemp[1].select('div:nth-of-type(3)')[0].text)
        departTime.append(routeTemp[2].select('div:nth-of-type(2)')[0].text)
        arriveTime.append(routeTemp[2].select('div:nth-of-type(4)')[0].text)
        paxOnBoard.append(routeTemp[4].select('div:nth-of-type(10)')[0].text)
        aircraftName.append(routeTemp[0].select('div:nth-of-type(4)')[0].text)
    except:
        print("error details")

fleet = []
aircraft = []
aircraftCheck = []
aircraftWear = []
yDemand = []
jDemand = []
fDemand = []

for ac in info:
    try:
        fleet.append(ac.find(id='ff-name').text)
        check = ac.find(
            class_='col-sm-6 bg-light border').contents[1].contents[1]
        wear = ac.find(
            class_='col-sm-6 bg-light border').contents[1].contents[3]
        demand = ac.findAll(class_='col-4 p-2 text-center exo')

        aircraftCheck.append(check.select('span:nth-of-type(6)')[0].text)
        aircraft.append(check.select('span:nth-of-type(2)')[0].text)
        aircraftWear.append(wear.select('span:nth-of-type(6)')[0].text)

        yclass = demand[3].contents[3] + demand[3].contents[4].text
        jclass = demand[4].contents[3] + demand[4].contents[4].text
        fclass = demand[5].contents[3] + demand[5].contents[4].text
        yDemand.append(re.sub('[^A-Za-z0-9/]+', '', yclass))
        jDemand.append(re.sub('[^A-Za-z0-9/]+', '', jclass))
        fDemand.append(re.sub('[^A-Za-z0-9/]+', '', fclass))
    except:
        print("Error info")

table = PrettyTable()

table.field_names = ["#", "A/C", 'A/C Name', "Hours to A-Check",
                     "Wear", 'Route Distance', 'Origin', 'Destination', 'Depart Time', 'Arrive Time', 'Fuel',
                     'Pax OnBoard', "Y Demand", "J Demand", "F Demand"]
for x in range(len(aircraftCheck)):
    try:
        table.add_row([x, aircraft[x], aircraftName[x], aircraftCheck[x],
                       str(aircraftWear[x]), routeDistance[x], origin[x], destination[x], departTime[x], arriveTime[x],
                       fuel[x], paxOnBoard[x], yDemand[x], jDemand[x], fDemand[x]])
    except:
        print("error table")
print(table)
