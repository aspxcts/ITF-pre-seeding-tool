import requests
import time
import json

rank_dict = {}
player_list = []
mapped_dict = {}


lastUpdateTime = '2/3/2025'
nextUpdateTime = '2/10/2025'

print(f"Rankings last updated: {lastUpdateTime}, Next update: {nextUpdateTime}")
tournament = input("enter tournament name (e.g. J100VEGAS): ")
date = input ("enter date of tournament start (DO NOT USE '/' !!): ")
tournamentList = input("enter tournament entry list URL (USE PROVIDED 'captureEntryURL.js' FILE!!!): ")
cookie = input("enter cookie (found when logging in, in the network tab): ")

with open('ranks.json', 'r') as f:
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
    "Cookie": cookie,
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

entries = get_entries(tournamentList)
entries = parse_entries(entries)

mapped_dict = map_ranks(ranks, entries)
sorted_dict = dict(sorted(mapped_dict.items(), key=get_value))

with open(f'seedingList-{tournament}-{date}.csv', 'w', encoding='utf-8') as f:
    f.write("name,rank,seed\n")
    for i, (name, rank) in enumerate(sorted_dict.items(), start=1):
        f.write(f"{name},{rank},{i}\n")

print(f"Seeding list saved to current directory as:{f}!")
