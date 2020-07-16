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
            for _ in days:
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
                    "%d",  member["flights"], grouping=True)
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

    return data


async def getAll():
    now = datetime.now()
    members = json.loads(contributionReq())
    data = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}
    message = ""
    message1 = ""
    message2 = ""
    message3 = ""
    message4 = ""
    message5 = ""
    i = 0
    for member in members["members"]:
        i += 1
        selectCompanySQL = f"SELECT * FROM members WHERE company ='{member['company']}'"
        mycursor.execute(selectCompanySQL)
        companyData = mycursor.fetchall()
        companyID = companyData[0][0]

        companyContrtibutionSQL = f"SELECT * FROM contribution WHERE companyID={companyID} AND data > '{now.year}-{now.month}-{now.day} '"
        mycursor.execute(companyContrtibutionSQL)
        companyContribution = mycursor.fetchall()

        yesterdayDate = now - timedelta(1)

        companyContrtibutionYesterdaySQL = f"SELECT * FROM contribution WHERE companyID = {companyID} AND  data between'{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 00:00' AND '{yesterdayDate.year}-{yesterdayDate.month}-{yesterdayDate.day} 23:59'"
        mycursor.execute(companyContrtibutionYesterdaySQL)
        companyContributionYesterday = mycursor.fetchall()

        days = [0,  0,  0, 0,  0,  0,  0,  0]

        for _ in days:
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

        if (len(companyContribution) >= 1):
            companyName = companyData[0][1]
            # data 0
            if(i <= 10):
                if (len(companyName) <= 13):
                    offset = (13-len(companyName))
                    message = message + companyName
                    for _ in range(offset+1):
                        message += " "
                elif (len(companyName) > 13):
                    string = companyName[:11] + '.. '
                    message = message + string

                if (len(str(companyData[0][3])) < 4):
                    offset = (4-len(str(companyData[0][3])))
                    message = message + str(companyData[0][3])
                    for _ in range(offset+1):
                        message += " "
                else:
                    message = message + str(companyData[0][3]) + " "

                string = f'${locale.format_string("%d", member["contributed"],grouping=True)} '
                if (len(string) < 10):
                    offset = (10-len(string))
                    message = message + string
                    for _ in range(offset+1):
                        message += " "
                else:
                    message = message + \
                        f'${locale.format_string("%d", member["contributed"],grouping=True)} '

                string = f'${locale.format_string("%d", total, grouping=True)} '
                if (len(string) < 8):
                    offset = (8-len(string))
                    message = message + string
                    for _ in range(offset+1):
                        message += " "
                else:
                    message = message + string
                if (len(companyContributionYesterday) > 0):
                    valor = companyContributionYesterday[len(
                        companyContributionYesterday) - 1][2]
                    valor2 = companyContributionYesterday[0][2]
                string = f'${locale.format_string("%d", member["contributed"]-valor,grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message = message + string
                    for _ in range(offset+1):
                        message += " "
                else:
                    message = message + string

                string = f'${locale.format_string("%d",valor-valor2 , grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message = message + string
                    for _ in range(offset+1):
                        message += " "
                else:
                    message = message + string
                message = message+"\n"
            # data 1
            elif(i > 10 and i <= 20):
                if (len(companyName) <= 13):
                    offset = (13-len(companyName))
                    message1 = message1 + companyName
                    for _ in range(offset+1):
                        message1 += " "
                elif (len(companyName) > 13):
                    string = companyName[:11] + '.. '
                    message1 = message1 + string

                if (len(str(companyData[0][3])) < 4):
                    offset = (4-len(str(companyData[0][3])))
                    message1 = message1 + str(companyData[0][3])
                    for _ in range(offset+1):
                        message1 += " "
                else:
                    message1 = message1 + str(companyData[0][3]) + " "

                string = f'${locale.format_string("%d", member["contributed"],grouping=True)} '
                if (len(string) < 10):
                    offset = (10-len(string))
                    message1 = message1 + string
                    for _ in range(offset+1):
                        message1 += " "
                else:
                    message1 = message1 + \
                        f'${locale.format_string("%d", member["contributed"],grouping=True)} '

                string = f'${locale.format_string("%d", total, grouping=True)} '
                if (len(string) < 8):
                    offset = (8-len(string))
                    message1 = message1 + string
                    for _ in range(offset+1):
                        message1 += " "
                else:
                    message1 = message1 + string
                if (len(companyContributionYesterday) > 0):
                    valor = companyContributionYesterday[len(
                        companyContributionYesterday) - 1][2]
                    valor2 = companyContributionYesterday[0][2]
                string = f'${locale.format_string("%d", member["contributed"]-valor,grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message1 = message1 + string
                    for _ in range(offset+1):
                        message1 += " "
                else:
                    message1 = message1 + string

                string = f'${locale.format_string("%d",valor-valor2 , grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message1 = message1 + string
                    for _ in range(offset+1):
                        message1 += " "
                else:
                    message1 = message1 + string
                message1 = message1+"\n"
             # data 2
            elif(i > 20 and i <= 30):
                if (len(companyName) <= 13):
                    offset = (13-len(companyName))
                    message2 = message2 + companyName
                    for _ in range(offset+1):
                        message2 += " "
                elif (len(companyName) > 13):
                    string = companyName[:11] + '.. '
                    message2 = message2 + string

                if (len(str(companyData[0][3])) < 4):
                    offset = (4-len(str(companyData[0][3])))
                    message2 = message2 + str(companyData[0][3])
                    for _ in range(offset+1):
                        message2 += " "
                else:
                    message2 = message2 + str(companyData[0][3]) + " "

                string = f'${locale.format_string("%d", member["contributed"],grouping=True)} '
                if (len(string) < 10):
                    offset = (10-len(string))
                    message2 = message2 + string
                    for _ in range(offset+1):
                        message2 += " "
                else:
                    message2 = message2 + \
                        f'${locale.format_string("%d", member["contributed"],grouping=True)} '

                string = f'${locale.format_string("%d", total, grouping=True)} '
                if (len(string) < 8):
                    offset = (8-len(string))
                    message2 = message2 + string
                    for _ in range(offset+1):
                        message2 += " "
                else:
                    message2 = message2 + string
                if (len(companyContributionYesterday) > 0):
                    valor = companyContributionYesterday[len(
                        companyContributionYesterday) - 1][2]
                    valor2 = companyContributionYesterday[0][2]
                string = f'${locale.format_string("%d", member["contributed"]-valor,grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message2 = message2 + string
                    for _ in range(offset+1):
                        message2 += " "
                else:
                    message2 = message2 + string

                string = f'${locale.format_string("%d",valor-valor2 , grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message2 = message2 + string
                    for _ in range(offset+1):
                        message2 += " "
                else:
                    message2 = message2 + string
                message2 = message2+"\n"
            # data 3
            elif(i > 30 and i <= 40):
                if (len(companyName) <= 13):
                    offset = (13-len(companyName))
                    message3 = message3 + companyName
                    for _ in range(offset+1):
                        message3 += " "
                elif (len(companyName) > 13):
                    string = companyName[:11] + '.. '
                    message3 = message3 + string

                if (len(str(companyData[0][3])) < 4):
                    offset = (4-len(str(companyData[0][3])))
                    message3 = message3 + str(companyData[0][3])
                    for _ in range(offset+1):
                        message3 += " "
                else:
                    message3 = message3 + str(companyData[0][3]) + " "

                string = f'${locale.format_string("%d", member["contributed"],grouping=True)} '
                if (len(string) < 10):
                    offset = (10-len(string))
                    message3 = message3 + string
                    for _ in range(offset+1):
                        message3 += " "
                else:
                    message3 = message3 + \
                        f'${locale.format_string("%d", member["contributed"],grouping=True)} '

                string = f'${locale.format_string("%d", total, grouping=True)} '
                if (len(string) < 8):
                    offset = (8-len(string))
                    message3 = message3 + string
                    for _ in range(offset+1):
                        message3 += " "
                else:
                    message3 = message3 + string
                if (len(companyContributionYesterday) > 0):
                    valor = companyContributionYesterday[len(
                        companyContributionYesterday) - 1][2]
                    valor2 = companyContributionYesterday[0][2]
                string = f'${locale.format_string("%d", member["contributed"]-valor,grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message3 = message3 + string
                    for _ in range(offset+1):
                        message3 += " "
                else:
                    message3 = message3 + string

                string = f'${locale.format_string("%d",valor-valor2 , grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message3 = message3 + string
                    for _ in range(offset+1):
                        message3 += " "
                else:
                    message3 = message3 + string
                message3 = message3+"\n"
            elif(i > 40 and i <= 50):
                if (len(companyName) <= 13):
                    offset = (13-len(companyName))
                    message4 = message4 + companyName
                    for _ in range(offset+1):
                        message4 += " "
                elif (len(companyName) > 13):
                    string = companyName[:11] + '.. '
                    message4 = message4 + string

                if (len(str(companyData[0][3])) < 4):
                    offset = (4-len(str(companyData[0][3])))
                    message4 = message4 + str(companyData[0][3])
                    for _ in range(offset+1):
                        message4 += " "
                else:
                    message4 = message4 + str(companyData[0][3]) + " "

                string = f'${locale.format_string("%d", member["contributed"],grouping=True)} '
                if (len(string) < 10):
                    offset = (10-len(string))
                    message4 = message4 + string
                    for _ in range(offset+1):
                        message4 += " "
                else:
                    message4 = message4 + \
                        f'${locale.format_string("%d", member["contributed"],grouping=True)} '

                string = f'${locale.format_string("%d", total, grouping=True)} '
                if (len(string) < 8):
                    offset = (8-len(string))
                    message4 = message4 + string
                    for _ in range(offset+1):
                        message4 += " "
                else:
                    message4 = message4 + string
                if (len(companyContributionYesterday) > 0):
                    valor = companyContributionYesterday[len(
                        companyContributionYesterday) - 1][2]
                    valor2 = companyContributionYesterday[0][2]
                string = f'${locale.format_string("%d", member["contributed"]-valor,grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message4 = message4 + string
                    for _ in range(offset+1):
                        message4 += " "
                else:
                    message4 = message4 + string

                string = f'${locale.format_string("%d",valor-valor2 , grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message4 = message4 + string
                    for _ in range(offset+1):
                        message4 += " "
                else:
                    message4 = message4 + string
                message4 = message4+"\n"
            else:
                if (len(companyName) <= 13):
                    offset = (13-len(companyName))
                    message5 = message5 + companyName
                    for _ in range(offset+1):
                        message5 += " "
                elif (len(companyName) > 13):
                    string = companyName[:11] + '.. '
                    message5 = message5 + string

                if (len(str(companyData[0][3])) < 4):
                    offset = (4-len(str(companyData[0][3])))
                    message5 = message5 + str(companyData[0][3])
                    for _ in range(offset+1):
                        message5 += " "
                else:
                    message5 = message5 + str(companyData[0][3]) + " "

                string = f'${locale.format_string("%d", member["contributed"],grouping=True)} '
                if (len(string) < 10):
                    offset = (10-len(string))
                    message5 = message5 + string
                    for _ in range(offset+1):
                        message5 += " "
                else:
                    message5 = message5 + \
                        f'${locale.format_string("%d", member["contributed"],grouping=True)} '

                string = f'${locale.format_string("%d", total, grouping=True)} '
                if (len(string) < 8):
                    offset = (8-len(string))
                    message5 = message5 + string
                    for _ in range(offset+1):
                        message5 += " "
                else:
                    message5 = message5 + string
                if (len(companyContributionYesterday) > 0):
                    valor = companyContributionYesterday[len(
                        companyContributionYesterday) - 1][2]
                    valor2 = companyContributionYesterday[0][2]
                string = f'${locale.format_string("%d", member["contributed"]-valor,grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message5 = message5 + string
                    for _ in range(offset+1):
                        message5 += " "
                else:
                    message5 = message5 + string

                string = f'${locale.format_string("%d",valor-valor2 , grouping=True)} '
                if (len(string) < 9):
                    offset = (9-len(string))
                    message5 = message5 + string
                    for _ in range(offset+1):
                        message5 += " "
                else:
                    message5 = message5 + string
                message5 = message5+"\n"

    data["0"] = message
    data["1"] = message1
    data["2"] = message2
    data["3"] = message3
    data["4"] = message4
    data["5"] = message5

    return data
