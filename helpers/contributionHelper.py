import mysql.connector
import requests
import json
from datetime import datetime, timedelta
import locale
import os
import re


from dotenv import load_dotenv
import matplotlib.pyplot as plt

from matplotlib import style
load_dotenv()


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="jet2data"
)
mycursor = mydb.cursor()

AM4_TOKEN = os.getenv("AM4_API_TOKEN")
locale.setlocale(locale.LC_ALL, 'en_US.utf8')


def contributionReq():
    response = requests.get(
        f'https://www.airline4.net/api/?access_token={AM4_TOKEN}&search=jet2%20alliance')
    if (response.status_code == 200):
        return response.text
    elif (response.status_code == 404):
        return 0


async def getOne(args):
    now = datetime.now()
    members = json.loads(contributionReq())

    data = {
        "name": "0",
        "days": "0",
        'total': '0',
        'avr': '0',
        'flights': '0',
        'fligthsAvr': '0',
        'contriFligth': '0',
        'share': '0',
        'totalReq': members["status"]["requests_remaining"],
        'place': 0,
        'diffYesterday': 0,
        'yesterday': 0,
        'flightYesterday': 0,
        'flightDiff': 0,
    }

    companyName = ''
    if (len(args) == 1):
        companyName = args[0]
    if (len(args) > 1):
        companyName = f'{args[0]} {args[1]}'

    for member in members["members"]:
        if (companyName.lower() in member["company"].lower()):

            selectCompanySQL = f"SELECT * FROM members WHERE company ='{member['company']}'"
            mycursor.execute(selectCompanySQL)
            companyData = mycursor.fetchall()
            companyID = companyData[0][0]

            companyContrtibutionSQL = f"SELECT * FROM contribution WHERE companyID={companyID} AND data > '{now.year}-{now.month}-{now.day} '"
            mycursor.execute(companyContrtibutionSQL)
            companyContribution = mycursor.fetchall()

            companyShareSQL = f"SELECT * FROM shares WHERE companyID={companyID} AND data > '{now.year}-{now.month}-{now.day}'"
            mycursor.execute(companyShareSQL)
            companyShare = mycursor.fetchall()

            companyFlightsSQL = f"SELECT * FROM flights WHERE companyID={companyID} AND data > '{now.year}-{now.month}-{now.day}'"
            mycursor.execute(companyFlightsSQL)
            companyFlights = mycursor.fetchall()

            yesterdayDate = now - timedelta(1)

            companyContrtibutionYesterdaySQL = f"SELECT * FROM contribution WHERE companyID = {companyID} AND  data between'{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 00:00' AND '{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 23:59'"
            mycursor.execute(companyContrtibutionYesterdaySQL)
            companyContributionYesterday = mycursor.fetchall()

            companyFlightsYesterdaySQL = f"SELECT * FROM flights WHERE companyID={companyID} AND  data between '{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 00:00' AND '{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 23:59'"
            mycursor.execute(companyFlightsYesterdaySQL)
            companyFlightsYesterday = mycursor.fetchall()

            days = [0,  0,  0, 0,  0,  0,  0,  0]
            i = 0
            for _ in days:
                i += 1
                yesterdayDate = now - timedelta(i)
                companyCSQL = f"SELECT * FROM contribution WHERE companyID = {companyID} AND  data between'{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 00:00' AND '{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 23:59'"
                mycursor.execute(companyCSQL)
                companyC = mycursor.fetchall()
                if (len(companyC) > 1):
                    days[len(days)-i] = companyC[len(
                        companyC) - 1][2] - companyC[0][2]

            total = 0
            for day in days:
                total = total + day
            plt.clf()
            names = ["1", "2", "3", "4", "5", "6", "7", "Yesterday"]
            yAxys = sorted(days)

            last = yAxys[7] + 2000

            i = 0
            for _ in yAxys:
                yAxys[i] = f'{locale.format_string("%d", yAxys[i],grouping=True)}'
                i += 1
            yAxys.insert(
                8, f'{locale.format_string("%d", last,grouping=True)}')

            i = 0
            for x in days:
                days[i] = f'{locale.format_string("%d", days[i],grouping=True)}'
                i += 1

            fig = plt.figure()

            plt.style.use('dark_background')
            ax = plt.axes()

            ax.plot([0, 0, 0, 0, 0, 0, 0, 0, 0], yAxys, color='black')
            # zip joins x and y co  ordinates in pairs
            for y, z in zip(names, days):
                label = z
                plt.annotate(label,  # this is the text
                             (y, z),  # this is the point to label
                             textcoords="offset points",  # how to position the text
                             # distance from text to points (x,y)
                             xytext=(0, 10),
                             ha='center')  # horizontal alignment can be left, right or center

            plt.plot(names, days, 'o-', label='curPerform', color='r')
            # plt.show()
            plt.savefig("online.png")
            plt.close(fig=fig)

            print(len(companyContribution))
            if (len(companyContribution) >= 1):

                contriDay = round(member["contributed"] / companyData[0][3], 2)
                fligthsDay = int(
                    companyFlights[len(companyFlights)-1][2] / companyData[0][3])
                contriFligth = round(
                    member["contributed"]/companyFlights[len(companyFlights)-1][2], 2)
                data["name"] = companyData[0][1]
                data["days"] = companyData[0][3]
                data["total"] = f'$ {locale.format_string("%d", member["contributed"],grouping=True)}'
                data['avr'] = f'$ {locale.format_string("%d", contriDay, grouping=True)}'
                data['flights'] = locale.format_string(
                    "%d",  companyFlights[len(companyFlights)-1][2], grouping=True)
                data['fligthsAvr'] = locale.format_string(
                    "%d", fligthsDay, grouping=True)
                data['contriFligth'] = f'$ {contriFligth}'
                data['share'] = f'$ {companyShare[len(companyShare)-1][2]}'
                data['place'] = f'$ {locale.format_string("%d", total, grouping=True)}'
                data['diffYesterday'] = f'$ {locale.format_string("%d", member["contributed"]-companyContributionYesterday[len(companyContributionYesterday)-1][2],grouping=True)}'
                data['yesterday'] = f'$ {locale.format_string("%d",companyContributionYesterday[len(companyContributionYesterday)-1][2]-companyContributionYesterday[0][2] , grouping=True)}'
                data['flightYesterday'] = locale.format_string(
                    "%d", companyFlightsYesterday[len(companyFlightsYesterday)-1][2] - companyFlightsYesterday[0][2], grouping=True)
                data['flightDiff'] = f'{locale.format_string("%d", member["flights"]-companyFlightsYesterday[len(companyFlightsYesterday)-1][2],grouping=True)}'
                print(data)
    return data
