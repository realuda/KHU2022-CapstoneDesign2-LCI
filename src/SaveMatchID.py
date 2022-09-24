import requests
import pprint
import pandas as pd
import datetime
import csv
import time

pp = pprint.PrettyPrinter(indent=4)
api_key = "RGAPI-97c35d4b-b840-4437-a5b7-1e7fb58a19fd"
request_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}


def match_v5_get_list_match_id(puuid, start, count):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    return requests.get(url, headers=request_header).json()

def get_match_id(puuid) :
    f = open('MatchId_data.csv', 'a', newline='')
    wr = csv.writer(f)
    for k in [0,100,200] :
        time.sleep(2)
        match_data = match_v5_get_list_match_id(puuid, k, 100)
        for i in match_data :
            wr.writerow([i])


sumname = pd.read_csv('D:/project_files/platinum_15000user.csv',encoding='cp949')
# print(league_df['summonerName'])
sumname=sumname['summonerName']
i = 1
error_list = []
for s_name in sumname :
    try:
        print(s_name, i)
        summoner_url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{s_name}"
        summoner_info = requests.get(summoner_url, headers=request_header)
        if summoner_info.status_code != 200:
            raise ValueError
        summoner_info = summoner_info.json()
        summoner_puuid = summoner_info['puuid']
        time.sleep(1)
        get_match_id(summoner_puuid)
        # if puuid.status_code==404 :
        #     raise ValueError
#         final_reulst.append(puuid)
#         time.sleep(1)
    except :
        print('제외됨')
        error_list.append(i)

    i += 1

print(error_list)