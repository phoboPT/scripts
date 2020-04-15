import requests
from bs4 import BeautifulSoup
import json


def getJoke():
    joke = requests.get(
        'https://jokes.guyliangilsing.me/retrieveJokes.php?type=dadjoke')

    if joke.status_code == 200:
        newJoke = json.loads(joke.text)
    elif joke.status_code == 404:
        print('Not Found id=144424')
    return newJoke
