import requests
import json


def getMembers():
    members = requests.get(
        'https://www.airline4.net/api/?access_token=klJLKFhweiuyOIsdbfW.ewrm8723LKjhdsQWtyudfnbLKUW&search=jet2%20alliance')

    if members.status_code == 200:
        newMembers = json.loads(members.text)
    elif members.status_code == 404:
        print('Not Found id=144424')
    return newMembers


def getInfo(name):
    members = requests.get(
        f'https://www.airline4.net/api/?access_token=klJLKFhweiuyOIsdbfW.ewrm8723LKjhdsQWtyudfnbLKUW&user={name}')

    if members.status_code == 200:
        newMembers = json.loads(members.text)
    elif members.status_code == 404:
        print('Not Found id=144424')
    return newMembers


"https://www.airline4.net/api/?access_token=klJLKFhweiuyOIsdbfW.ewrm8723LKjhdsQWtyudfnbLKUW&user=phobo%20inc"

print("started")
members = getMembers()
membersName = []
for x in members["members"]:
    memberInfo = getInfo(x["company"])["fleet"]
    f = open(f"fleet.txt", "a")
    f.write(f'Company: {x["company"]}\n')
    for y in memberInfo:
        f.write(f'A/C {y["aircraft"]} Ammount: {y["amount"]}\n')
    f.close

print("finished")
