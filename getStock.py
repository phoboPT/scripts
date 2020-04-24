import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
load_dotenv()
MY_COOKIE = os.getenv("MY_COOKIE")

stock = requests.get(
    'https://am4.pagespeedster.com/am4/json/userChart.php?id=144424',
    headers={
        'User-Agent': 'Super Cool Browser',
        'cookie': 'device=app; deviceType=android; ' + MY_COOKIE},
)
if stock.status_code == 200:
    stockInfo = stock.text
elif stock.status_code == 404:
    print('Not Found id=144424')


parsed_json = (json.loads(stockInfo))

plt.plot(parsed_json['time'], parsed_json['data'])
plt.ylabel('Value')
plt.xlabel('Time')

for a, b in zip(parsed_json['time'], parsed_json['data']):
    plt.text(a, b, str(b), ha="center")
plt.show()
