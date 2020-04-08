import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sched
import time
import re

sleepTime = 0


def getFuelData():
    return requests.get(
        'https://am4.pagespeedster.com/am4/fuel.php?fbSig=false&_=1584038619891',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )


def getCo2Data():
    return requests.get(
        'https://am4.pagespeedster.com/am4/co2.php?fbSig=false&_=1584038619905',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )


def sendRequestCo2(amount):
    requests.get(
        'https://www.airline4.net/co2.php?mode=do&amount=' +
        amount+'&fbSig=false&_=1584653902786',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )


def sendRequestFuel(amount):
    requests.get(
        'https://www.airline4.net/fuel.php?mode=do&amount=' +
        amount+'&fbSig=false&_=1584653902786',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )


def buyFuel():
    global sleepTime
    fuelHTML = getFuelData()

    if fuelHTML.status_code == 200:
        fuelInfo = BeautifulSoup(fuelHTML.text, 'html.parser')
    elif fuelHTML.status_code == 404:
        print('Not Found id=144424')

    fuelPrice = int(
        re.sub('[,]+', '', fuelInfo.find("span", id="sumCost").text))
    amountToBuy = int(re.sub(
        '[,]+', '', fuelInfo.find("span", id="remCapacity").text))

    if (amountToBuy < 1):
        sleepTime = 1800
        print(f"Tank of Fuel full sleep for {int(sleepTime/60)}")
    elif (fuelPrice < 600):
        sendRequestFuel(str(amountToBuy))
        sleepTime = 300
        print(f"buy fuel at {fuelPrice} sleep for {int(sleepTime/60)}")
    else:
        sleepTime = 1800
        print(
            f"Fuel to expensive {fuelPrice} need {amountToBuy} sleep for {int(sleepTime/60)}")


def buyCo2():
    global sleepTime
    co2 = getCo2Data()

    if co2.status_code == 200:
        co2Info = BeautifulSoup(co2.text, 'html.parser')
    elif co2.status_code == 404:
        print('Not Found id=144424')

    co2Price = int(
        re.sub('[,]+', '', co2Info.find("span", id="sumCost").text))
    amountToBuy = int(re.sub(
        '[,]+', '', co2Info.find("span", id="remCapacity").text))

    if (amountToBuy < 1):
        if (sleepTime > 300):
            sleepTime = 1800
        print(f"Tank of CO2 full sleep for {int(sleepTime/60)}")
    elif (co2Price < 140):
        sendRequestCo2(str(amountToBuy))
        if (sleepTime > 300):
            sleepTime = 300
        print(
            f"buyed {amountToBuy} of CO2 at {co2Price} sleep for  {int(sleepTime/60)}")
    else:
        if (sleepTime > 300):
            sleepTime = 1800
        print(
            f"Co2 to expensive {co2Price} need {amountToBuy} sleep for {int(sleepTime/60)}")


while True:
    buyFuel()
    buyCo2()
    time.sleep(sleepTime)
