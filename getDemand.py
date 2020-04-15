import requests
from bs4 import BeautifulSoup


def getCo2Data(dist, id):
    response = requests.get(
        f'https://am4.pagespeedster.com/am4/research_main.php?mode=search&rwy=1&dist={dist}&depId={id}&arr=0',
        headers={
            'User-Agent': 'Super Cool Browser',
            'cookie': 'device=app; deviceType=android; PHPSESSID=uha1demuouq896v2kvmi6u8s4m'},
    )
    if (response.status_code == 200):
        res = BeautifulSoup(response.text, 'html.parser')
    elif response.status_code == 404:
        print('Not Found id=')

    return res


def getInfo():

    fDemand = 250
    for i in range(3981):
        dist = 0
        name = getCo2Data(1000, i+1)
        fileName = name.select(
            " #list > div:nth-child(1) > div:nth-child(1) > div > b:nth-child(1)")
        for y in range(42):
            dist = dist+500
            html = getCo2Data(dist, i+1)
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
                    # if(int(f[0].text) > fDemand):
                    print(
                        f'route: {route[0].text} distance: {distance[0].text}')
                    print(f"E: {e[0].text} B: {b[0].text} F: {f[0].text}")
                    string = f"route: {route[0].text} distance: {distance[0].text}\n E: {e[0].text} B: {b[0].text} F: {f[0].text}\n"

                    f = open(f"{fileName[0].text}.txt", "a")
                    f.write(string)
                    f.close
                except:
                    continue


getInfo()
