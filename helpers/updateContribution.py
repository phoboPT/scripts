import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime, timedelta
import json
import locale
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
AM4_TOKEN = os.getenv("AM4_API_TOKEN")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="jet2data"
)
mycursor = mydb.cursor()


def calcContri():
    now = datetime.now()
    allData = []
    members = json.loads(getContributions())
    resetDate = datetime(2020, 3, 16)

    for x in members["members"]:
        data = {
            "name": "",
            "days": "",
            'total': '',
            'flights': x['flights'],
            'dailyContribution': x["dailyContribution"],
            'shareValue': x["shareValue"]
        }

        delta = int((now - resetDate).days)

        delta2 = now - datetime.fromtimestamp(x['joined'])

        if (int(delta2.days) < int(delta)):
            delta = delta2.days

        data["name"] = x["company"]
        data["days"] = delta
        data["joined"] = x["joined"]
        data["total"] = x["contributed"]

        allData.append(data)
    return allData


async def saveSheet(ctx, channel):

    data = calcContri()

    for player in data:
        await ctx.send(f'updating {player["name"]}')

        newUser = (player['name'], player['joined'], player['days'])
        newContribution = (player['total'])
        sqlInsertNewMember = "INSERT INTO members(company, joined,days)VALUES(%s,%s,%s)"
        sqlInsertNewContribution = "INSERT INTO contribution(companyID, contributed,dailyContribution)VALUES(%s,%s,%s)"
        sqlInsertNewFlight = "INSERT INTO flights(companyID, flights)VALUES(%s,%s)"
        sqlInsertNewShare = "INSERT INTO shares(companyID, shareValue)VALUES(%s,%s)"

        selectData = f"SELECT * FROM members WHERE company ='{player['name']}'"

        mycursor.execute(selectData)
        result = mycursor.fetchall()
        if len(result) == 0:
            mycursor.execute(sqlInsertNewMember, newUser)
            mycursor.execute(selectData)
            result = mycursor.fetchall()
        sqlUpdateNewMember = f"UPDATE members SET days ={player['days']} WHERE id ={result[0][0]}"
        mycursor.execute(sqlUpdateNewMember)
        newContribution = (result[0][0], player['total'],
                           player['dailyContribution'])
        newFlight = (result[0][0], player['flights'])
        newShare = (result[0][0], player['shareValue'])
        mycursor.execute(sqlInsertNewContribution, newContribution)
        mycursor.execute(sqlInsertNewFlight, newFlight)
        mycursor.execute(sqlInsertNewShare, newShare)
        mydb.commit()
        # roleId = '<@&725037141138210878>'

        # string = f"{roleId} "
        # string = string+f"The contribution for {player['name']} is {day} "

        # day = re.sub('[$,]', '', day)

        # if (int(day) <= 0):
        #     await channel.send(string)


def getContributions():
    response = requests.get(
        f'https://www.airline4.net/api/?access_token={AM4_TOKEN}&search=jet2%20alliance')
    if (response.status_code == 200):
        return response.text
    elif (response.status_code == 404):
        return 0


# saveSheet()
