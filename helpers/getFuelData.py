import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()
AM4_SCRAPPING_COOKIE = os.getenv("AM4_SCRAPPING_COOKIE")


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
