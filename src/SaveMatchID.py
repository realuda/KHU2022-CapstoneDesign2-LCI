#puuid에서 matchId 가져오기(중복x)
import json
import requests
import pandas as pd
import time
import datetime
from requests.adapters import HTTPAdapter, Retry

#api키 읽어오기
f = open("../key.txt",'r')
api_key = f.readline()

day_WantToGet = 14   #구하고자 하는 날

day = 86400    #하루 타임스탬프
day_left = 86400*day_WantToGet  #남은 날짜 계산용 변수

puuidList = [] #챌린저 유저 puuid 저장하는 list
matchList = set() #챌린저 유저의 matchId 저장하는 set

current = datetime.datetime.now().timestamp() #현재 timestamp
wantAgo = str(int(current)-day_left) #원하는 날의 첫 날 timestamp


#csv 파일 읽어오기(puuid만 list로 저장)
df = pd.read_csv('challengerID.csv', encoding = 'utf-8-sig') #챌린저 유저 정보가 담긴 csv file read
puuidList = df['puuId']

#request보낼때마다 +1
count = 0
err_count = list()

#시작시간
start = time.time()

#puuid에서 matchId 가져오기
for userPid in puuidList:
    tempDay = day_WantToGet #구하려는 날 임시 저장용 변수
    temp2 = 0 #며칠씩 가져올지 구하는 임시 변수
    tempAgo = wantAgo #남은 날짜 계산하는 임시 변수

    while tempDay>0:
        
        if tempDay>3:
            temp2 = 3
        else:
            temp2 = tempDay

        #100번째마다 시간 검사
        if count%100 == 0 and count != 0:
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

            #요청 URL. 최대 매치id를 100개밖에 못가져와서 3일씩 계산함
            #10초에 500requests
            URL = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?startTime={1}&endTime={2}&type=ranked&count=100'.format(userPid, tempAgo, str(int(tempAgo)+day*temp2))
            res = session.get(URL, headers = {"X-Riot-Token": api_key })

        except requests.exceptions.ConnectionError:
            print('Connection error occured')

        #성공
        if res.status_code == 200:
            matchId = json.loads(res.text)

            for i in matchId:
                matchList.add(i)

            tempDay = tempDay - temp2   #점점 3일씩 줄여나가다가 다 가져오면 끝
            tempAgo = str(int(tempAgo)+day*temp2)

            count += 1
            print("Done " + str(count))
        
            #time.sleep(1.2) #한 번에 많은 요청을 보내면 거부해서 2초의 시간차를 둠
        #실패
        else:
            err_count.append(count)
            count += 1
            print("error occured. check your api key or input")    



#matchId csv로 저장
df = pd.DataFrame(list(matchList), columns = ['matchId'])
df.to_csv("ChallengerMatchID.csv", index = False, encoding = 'utf-8-sig')

print(err_count)