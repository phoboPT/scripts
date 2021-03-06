from selenium import webdriver
import re
import time
from dotenv import load_dotenv
import os
from random import randrange
load_dotenv()
MY_TOKEN = os.getenv("MY_TOKEN")
MY_EMAIL = os.getenv("MY_EMAIL")

starttime = time.time()
sleepTime = 10

options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(options=options)
#  browser = webdriver.Chrome()


def checkMarkting(browser):
    browser.find_elements_by_css_selector(
        "[title*='Staff, Marketing']")[0].click()

    browser.implicitly_wait(60)
    browser.find_element_by_css_selector('#popBtn2').click()

    marktingCampaign = browser.find_element_by_css_selector('#marketingMain')
    activeMarketing = getMarktingAtive(browser, marktingCampaign)

    if (activeMarketing != 2):
        buyMarketing(browser, activeMarketing)

    browser.find_element_by_css_selector(
        '#popup > div > div > div.modal-header > div > span').click()

    departFlights(browser)


def buyMarketing(marketingTab, activeMarketing):
    if (activeMarketing == 0):
        marketingTab.find_element_by_css_selector(
            '#newCampaign').click()
        marketingTab.implicitly_wait(60)
        marketingTab.find_element_by_css_selector(
            '#campaign-1 > table > tbody > tr:nth-child(1) > td:nth-child(1)').click()
        marketingTab.implicitly_wait(60)
        marketingTab.find_elements_by_css_selector(
            '# campaign-1 > table > tbody > tr:nth-child(1)').selectByIndex(5)
        marketingTab.find_elements_by_css_selector('#c4Btn').click()
        marketingTab.implicitly_wait(60)
        print("Arline Marketing Purchased")
        activeMarketing = 1

    if(activeMarketing == 1):
        marketingTab.find_element_by_css_selector(
            '#newCampaign').click()

        marketingTab.implicitly_wait(60)
        marketingTab.find_element_by_css_selector(
            '#campaign-1 > table > tbody > tr:nth-child(3) > td:nth-child(2)').click()
        marketingTab.implicitly_wait(60)
        marketingTab.find_element_by_css_selector(
            '#marketingStart > table > tbody > tr > td.text-right > button').click()

        marketingTab.implicitly_wait(60)
        print("Eco Marketing Purchased")


def getMarktingAtive(browser, marktingCampaign):
    # get the marketing
    rep = 0
    if ("Airline reputation" in marktingCampaign.text):

        rep = 1
    if ("Eco friendly" in marktingCampaign.text):
        rep = 2

    print(f"Marketing {re.sub('[a-z A-Z]+', '', marktingCampaign.text)}")
    return rep


def departFlights(browser):
    global sleepTime
    departButton = browser.find_element_by_css_selector(
        '#listDepartAll > div > button')
    departNumber = departButton.text

    if(departNumber):
        departNumber = int(re.sub('[Depart ]+', '', departNumber))
        if (departNumber):
            if(departNumber > 0):
                departButton.click()
                browser.implicitly_wait(60)
                amountGained = browser.find_element_by_css_selector(
                    '#fd_income').text
                print(
                    f'Sended {departNumber} planes, totalling {amountGained} ')
    else:
        print('Sem avioes para enviar')

    if(departNumber == 20):
        sleepTime = 10

    else:
        sleepTime = randrange(300, 600)


while True:
    teste = 0
    if (teste == 0):
        browser.get(
            f'https://am4.pagespeedster.com/am4/?gameType=app&uid={MY_EMAIL}&uid_token={MY_TOKEN}&mail={MY_EMAIL}&mail_token={MY_TOKEN}')

    try:
        checkMarkting(browser)
        print(f"wait {sleepTime/60} minutes")
        teste = 1
    except:
        sleepTime = 100
        print("something went wrong")

    time.sleep(sleepTime)
