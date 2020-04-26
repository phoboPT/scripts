import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
load_dotenv()
AM4_SCRAPPING_COOKIE = os.getenv("AM4_SCRAPPING_COOKIE")


def getDemandHTML(dist, id):
    response = requests.get(
        f'https://www.airline4.net/research_main.php?mode=search&rwy=1&dist={dist}&depId={id}&arr=0',
        headers={'User-Agent': 'browser',
                 'cookie':  AM4_SCRAPPING_COOKIE},
    )
    if (response.status_code == 200):
        res = BeautifulSoup(response.text, 'html.parser')
    elif response.status_code == 404:
        print('Not Found id=')

    return res


def getInfo():
    fDemand = 250
    bDemand = 300
    eDemand = 1500
    distanceRange = 13500

    # airportList = [2027, 865, 150, 1661, 2763, 3911, 1440, 3500, 3731, 2499]
    airportList = [3499]
    for i in airportList:
        dist = 0
        name = getDemandHTML(1000, i)

        fileName = name.select(
            "#list > div:nth-child(1) > div:nth-child(1) > div > b:nth-child(1)")
        for y in range(44):
            dist = dist + 500
            print(f'serarching for {dist}')
            html = getDemandHTML(dist, i)
            for x in range(50):
                route = html.select(
                    f"#list > div:nth-child({x}) > div:nth-child(1) > div")
                distance = html.select(
                    f"#list > div:nth-child({x}) > div.col-6.m-text.text-right > div > b")
                e = html.select("#list")[0].select(
                    f'div:nth-child({x})> div:nth-child(3)>b')
                b = html.select("#list")[0].select(
                    f'div:nth-child({x})> div:nth-child(4)>b')
                f = html.select("#list")[0].select(
                    f'div:nth-child({x})> div:nth-child(5)>b')
                try:
                    # newDis = re.sub('[,km]+', '', distance[0].text)
                    # print(
                    #     f'route: {route[0].text} distance: {newDis}')

                    # if (int(newDis) < distanceRange):
                    #     if (int(f[0].text) > fDemand):
                    #         print(
                    #             f"E: {e[0].text} B: {b[0].text} F: {f[0].text}")
                    #         string = f"route: {route[0].text} distance: {distance[0].text}\n E: {e[0].text} B: {b[0].text} F: {f[0].text}\n"

                    #         f = open(f"{fileName[0].text}.txt", "a")
                    #         f.write(string)
                    #         f.close
                    # if (int(newDis) > distanceRange):
                    #     if(int(b[0].text) > bDemand):
                    #         print(
                    #             f'route: {route[0].text} distance: {distance[0].text}')
                    #         print(
                    #             f"E: {e[0].text} B: {b[0].text} F: {f[0].text}")
                    #         string = f"route: {route[0].text} distance: {distance[0].text}\n E: {e[0].text} B: {b[0].text} F: {f[0].text}\n"

                    #         f = open(f"{fileName[0].text}.txt", "a")
                    #         f.write(string)
                    #         f.close
                    # if(int(e[0].text) > eDemand):
                    print(
                        f'route: {route[0].text} distance: {distance[0].text}')
                    print(
                        f"E: {e[0].text} B: {b[0].text} F: {f[0].text}")
                    string = f"route: {route[0].text} distance: {distance[0].text}\n E: {e[0].text} B: {b[0].text} F: {f[0].text}\n"

                    f = open(f"{fileName[0].text}.txt", "a")
                    f.write(string)
                    f.close

                except:
                    continue


getInfo()
