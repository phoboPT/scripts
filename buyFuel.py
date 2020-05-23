import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sched
import time
import re
from dotenv import load_dotenv
import os
load_dotenv()
CO2_PRICE = int(os.getenv("FUEL_PRICE"))
FUEL_PRICE = int(os.getenv("CO2_PRICE"))
MY_COOKIE = os.getenv("MY_COOKIE")
sleepTime = 0


def getFuelData():
    return requests.get(
        'https://www.airline4.net/fuel.php?fbSig=false&_=1584038619891',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; ' + MY_COOKIE},
    )


def getCo2Data():
    return requests.get(
        'https://www.airline4.net/co2.php?fbSig=false&_=1584038619905',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; ' + MY_COOKIE},
    )


def sendRequestCo2(amount):
    requests.get(
        'https://www.airline4.net/co2.php?mode=do&amount=' +
        amount+'&fbSig=false&_=1584653902786',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; ' + MY_COOKIE},
    )


def sendRequestFuel(amount):
    requests.get(
        'https://www.airline4.net/fuel.php?mode=do&amount=' +
        amount+'&fbSig=false&_=1584653902786',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; ' + MY_COOKIE},
    )


def buyFuel():

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
        print(f"Tank of Fuel full")
    elif (fuelPrice < FUEL_PRICE):
        sendRequestFuel(str(amountToBuy))

        print(f"buy fuel at {fuelPrice} ")
    else:

        print(
            f"Fuel to expensive {fuelPrice} need {amountToBuy}")


def buyCo2():

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

        print(f"Tank of CO2 full ")
    elif (co2Price < CO2_PRICE):
        sendRequestCo2(str(amountToBuy))

        print(
            f"buyed {amountToBuy} of CO2 at {co2Price}   ")
    else:

        print(
            f"Co2 to expensive {co2Price} need {amountToBuy} ")


while True:
    try:
        sleepTime = 1800
        buyFuel()
        buyCo2()
    except:
        sleepTime = 10

    time.sleep(sleepTime)
