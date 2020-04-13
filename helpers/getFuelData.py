import requests
from bs4 import BeautifulSoup


def getFuelPrice():
    fuelHTML = requests.get(
        'https://am4.pagespeedster.com/am4/fuel.php?fbSig=false&_=1584038619891',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )

    if fuelHTML.status_code == 200:
        fuelInfo = BeautifulSoup(fuelHTML.text, 'html.parser')
    elif fuelHTML.status_code == 404:
        print('Not Found id=144424')
    return fuelInfo.find("span", id="sumCost").text


def getC02Price():
    co2HTML = requests.get(
        'https://am4.pagespeedster.com/am4/co2.php?fbSig=false&_=1584038619905',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )

    if co2HTML.status_code == 200:
        co2HTML = BeautifulSoup(co2HTML.text, 'html.parser')
    elif co2HTML.status_code == 404:
        print('Not Found id=144424')
    return co2HTML.find("span", id="sumCost").text
