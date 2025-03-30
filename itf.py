from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import requests
import time
import json

options = {'enable_har': True,}

rank_dict = {}
player_list = []
mapped_dict = {}

found_cookie = None
found_url = None

lastUpdateTime = '2/10/2025'
nextUpdateTime = '2/17/2025'

driver = webdriver.Chrome(seleniumwire_options=options)
driver.get("https://ipin.itftennis.com")

rankfilename = input("enter file name with .json: ")
input("Hit enter once you have navigated to the tournament you want to check the seeding for! ")

tournamentName = driver.find_element(By.XPATH, "/html/body/main/div/div/div/header/h1").text
date = driver.find_element(By.XPATH, "/html/body/main/div/div/div/header/div").text

for request in driver.requests:
    if request.url.startswith("https://ipin.itftennis.com/Umbraco/Surface/entrylist/entry-list?tennisEventId"):
        cookies = request.headers.get('Cookie')
        if cookies:
            found_url = request.url
            found_cookie = cookies
            break

if found_cookie:
    print("Scraping Successful!")
else:
    print("No matching URL or cookie detected.")

driver.quit()

print(f"Rankings last updated: {lastUpdateTime}, Next update: {nextUpdateTime}")
time.sleep(0.5)
print(f"Tournament selected: {tournamentName}")
time.sleep(0.5)
print(f"Date period: {date}")
time.sleep(0.5)
print("Computing...")

with open(rankfilename, 'r') as f:
    ranks = json.load(f)

headers_entry = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Priority":"u=1, i",
    "Referer":"https://ipin.itftennis.com/entries?tournamentId=0e0d03f3-8bf2-4a65-9e22-588d22210f4e&circuitId=4a17c0c7-3dd4-4193-b868-dadfdf16732f",
    "Host": "ipin.itftennis.com",
    "Sec-ch-ua-platform":"Windows",
    "Sec-fetch-dest":"empty",
    "Sec-fetch-mode":"cors",
    "Sec-fetch-site":"same-origin",
    "Sec-fetch-user":"?1",
    "Upgrade-insecure-requests":"1",
    "Cookie": found_cookie,
}

def get_entries(url):
    try:
        response = requests.get(url, headers=headers_entry)
        time.sleep(2)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error!: '. response.status_code)
            return None
    except Exception as e:
        print("Error!: ", e)
        return None

def parse_entries(data):
    print(data)
    for i in range(len(data['entryLists'][0]['sections'][0]['entries'])):
        try:
            player_list.append(data['entryLists'][0]['sections'][0]['entries'][i]['players'][0]['person']['familyName'] + " " + data['entryLists'][0]['sections'][0]['entries'][i]['players'][0]['person']['givenName'])
        except Exception as e:
            print(e)
            break
    return player_list

def map_ranks(ranks, entries):
    for i in range(len(entries)):
        try:
            mapped_dict[entries[i]] = ranks[entries[i]]
        except KeyError as e:
            print(e)
            mapped_dict[entries[i]] = 99999
            continue
    return mapped_dict

def get_value(item):
    return item[1]

entries = get_entries(found_url)
entries = parse_entries(entries)

mapped_dict = map_ranks(ranks, entries)
sorted_dict = dict(sorted(mapped_dict.items(), key=get_value))

with open(f'seedingList-{tournamentName}-{date}.csv', 'w', encoding='utf-8') as f:
    f.write("name,rank,seed\n")
    for i, (name, rank) in enumerate(sorted_dict.items(), start=1):
        f.write(f"{name},{rank},{i}\n")

print(f"Seeding list saved to current directory as:{f}!")
