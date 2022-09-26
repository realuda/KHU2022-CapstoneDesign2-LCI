#puuid에서 matchId 가져오기(중복x)
import json
import requests
import pandas as pd
import time
import datetime

api_key = 'RGAPI-dda2952f-6b50-4bb2-b17f-804c0eb83bf5'

week = 86400*7 #일주일 타임스탬프

puuidList = [] #챌린저 유저 puuid 저장하는 list
matchList = set() #챌린저 유저의 matchId 저장하는 set

current = datetime.datetime.now().timestamp() #현재 timestamp
weekago = str(int(current)-week) #일주일 전 timestamp

#URL = https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/GFuRfwdmM24SOsfs3OpSYrs8u0qKJntEgsjnp3y97_K2a0bEYTU3IX79jL2VTjTvL6XNDBrmGb4UWA/ids?startTime=1663522807&type=ranked&start=0&count=20
#res = requests.get(URL, headers = {"X-Riot-Token": api_key })

#csv 파일 읽어오기(puuid만 list로 저장)
df = pd.read_csv('challengerID.csv', encoding = 'utf-8-sig') #챌린저 유저 정보가 담긴 csv file read
puuidList = df['puuId']


#puuid에서 matchId 가져오기

for userPid in puuidList:
    #한 번에 많은 요청을 보내면 거부해서 2초의 시간차를 둠
    time.sleep(2)
    

    #요청 URL
    URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?startTime={1}&type=ranked&count=100'.format(userPid, weekago)
    res = requests.get(URL, headers = {"X-Riot-Token": api_key })

    #성공
    if res.status_code == 200:
        matchId = json.loads(res.text)

        for i in matchId:
            matchList.add(i)

        
        print("Done")
    
    #실패
    else:
        print("URL 접근 실패")

#matchId csv로 저장
df = pd.DataFrame(list(matchList), columns = ['matchId'])
df.to_csv("ChallengerMatchID.csv", index = False, encoding = 'utf-8-sig')