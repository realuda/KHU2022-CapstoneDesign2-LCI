#챌린저 유저 id 찾고 csv 파일로 저장
import json
import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
import time

#api키 읽어오기
f = open("../key.txt",'r')
api_key = f.readline()

tier_list = ['CHALLENGER', 'GRANDMASTER']

sidList = []
sNameList = []
puuidList = []

#request보낼 때마다 +1
count = 0
err_count = list()

#시작시간
start = time.time()

#https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&api_key=RGAPI-8bec98f4-864f-4334-81d7-0647e3c314fd

for tier in tier_list:

    if tier == 'CHALLENGER':
        page = 2
    elif tier == 'GRANDMASTER':
        page = 4

    for page in range(0,page):
        #티어에 따른 유저 정보(이름, sid)를 가져온다.
        URL = 'https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/'+tier+'/I?page='+str(page+1)
        res = requests.get(URL, headers = {"X-Riot-Token": api_key })

        count += 1

        if res.status_code == 200:
            
            resobj = json.loads(res.text)
            for i in resobj:
                #print(i["summonerName"])
                sNameList.append(i["summonerName"])
                sidList.append(i["summonerId"])

                #2분 최대 100회의 request만 수행한다
                if count%100 == 0:
                    now_time = time.time()  #얼마나 지났나
                    time.sleep(120-(now_time-start)) #120초에서 경과시간을 뺀 만큼 sleep. 경과시간 = now_time-start
                    start = time.time() #start 다시 설정

                try:
                    #request 초과 에러 방지용
                    session = requests.Session()
                    retry = Retry(connect = 10, backoff_factor=1)
                    adapter = HTTPAdapter(max_retries=retry)
                    session.mount('http://', adapter)
                    session.mount('https://', adapter)

                    #sid로 puuid가져오기. 2분 최대 100회
                    URL2 = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/"+i["summonerId"]
                    res2 = session.get(URL2, headers = {"X-Riot-Token": api_key})
                    #time.sleep(1.2)

                except requests.exceptions.ConnectionError:
                    print('Connection error occured')

                if res2.status_code == 200:   

                    challengerInfo = json.loads(res2.text)
                    #print(challengerInfo["puuid"])
                    
                    count+=1
                    print("Done "+str(count) + "/1000") #챌+그마 유저 1000명
                    puuidList.append(challengerInfo["puuid"])

                else:
                    err_count.append(count)
                    count+=1
                    print("error occured. check your api key or input")

        else:
            print("error occured. check your api key or input")    


#저장
df = pd.DataFrame(sNameList,columns = ['summonerName'])
df['summonerId'] = sidList
df['puuId'] = puuidList

df.to_csv("ChallengerID.csv", index = False, encoding ='utf-8-sig')

print(err_count)