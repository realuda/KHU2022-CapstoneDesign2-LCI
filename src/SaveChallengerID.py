#챌린저 유저 id 찾고 csv 파일로 저장
import json
import requests
import pandas as pd
import time

#api키 읽어오기
f = open("../key.txt",'r')
api_key = f.readline()

tier = 'CHALLENGER' #티어 
tier2 = 'GRANDMASTER'

URL = 'https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/'+tier+'/I'
res = requests.get(URL, headers = {"X-Riot-Token": api_key })

sidList = []
sNameList = []
puuidList = []

if res.status_code == 200:
    resobj = json.loads(res.text)
    for i in resobj:
        print(i["summonerName"])
        sNameList.append(i["summonerName"])
        sidList.append(i["summonerId"])


        #puuid가져오기. 1분에 1600 requests
        URL2 = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"+i["summonerId"]
        res2 = requests.get(URL2, headers = {"X-Riot-Token": api_key})
        #time.sleep(1.2)
        challengerInfo = json.loads(res2.text)
        print(challengerInfo["puuid"])
        puuidList.append(challengerInfo["puuid"])

    df = pd.DataFrame(sNameList,columns = ['summonerName'])
    df['summonerId'] = sidList
    df['puuId'] = puuidList

    df.to_csv("ChallengerID.csv", index = False, encoding ='utf-8-sig')

else:
    print("키가 잘못됨")    