"""
필요한 데이터는 승리 챔피언, 패배 챔피언
input 1개의 매치 데이터
output 승리 챔피언 5명 패배 챔피언 5명 + 밴 챔피언 10명

info 안에 teams 안에 bans 안에 밴한 championId 있음 밴 안했으면 -1

info안에 participants list 안에 championId랑 win 있음

결과 표기
챔피언id/승 수/패배 수/밴 수 
+
챔피언 column : 승 / 패

열 챔피언, 행 챔피언
행 챔피언win, 챔피언lose까지 엄청 많이 필요함

승리한 챔피언이다 -> 같은 팀원 찾아서 win에 +1
패배한 챔피언이다 -> 같은 팀원 찾아서 lose에 +1

"""

import json
import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
import time

#매치 수
matchCount = 5414

#api키 읽어오기
f = open("../key.txt",'r')
api_key = f.readline()

#챔피언Id와 승,패,밴 수를 저장할 dictory 초기화
champ_result = {266:[0,0,0,"아트록스"], 103:[0,0,0, "아리"], 84:[0,0,0,"아칼리"], 166:[0,0,0,"아크샨"], 12:[0,0,0,"알리스타"], 32:[0,0,0,"아무무"], 34:[0,0,0,"애니비아"], 1:[0,0,0,"애니"], 523:[0,0,0,"아펠리오스"], 
                22:[0,0,0,"애쉬"], 136:[0,0,0,"아우렐리온 솔"], 268:[0,0,0,"아지르"], 432:[0,0,0,"바드"], 200:[0,0,0,"벨베스"], 53:[0,0,0,"블리츠크랭크"], 63:[0,0,0,"브랜드"], 201:[0,0,0,"브라움"], 51:[0,0,0,"케이틀린"], 164:[0,0,0,"카밀"], 
                69:[0,0,0,"카시오페아"], 31:[0,0,0,"초가스"], 42:[0,0,0,"코르키"], 122:[0,0,0,"다리우스"], 131:[0,0,0,"다이애나"], 119:[0,0,0,"드레이븐"], 36:[0,0,0,"문도 박사"], 245:[0,0,0,"에코"], 60:[0,0,0,"엘리스"], 28:[0,0,0,"이블린"], 
                81:[0,0,0,"이즈리얼"], 9:[0,0,0,"피들스틱"], 114:[0,0,0,"피오라"], 105:[0,0,0,"피즈"], 3:[0,0,0,"갈리오"], 41:[0,0,0,"갱플랭크"], 86:[0,0,0,"가렌"], 150:[0,0,0,"나르"], 79:[0,0,0,"그라가스"], 104:[0,0,0,"그레이브즈"], 
                887:[0,0,0,"그웬"], 120:[0,0,0,"헤카림"], 74:[0,0,0,"하이머딩거"], 420:[0,0,0,"일라오이"], 39:[0,0,0,"이렐리아"], 427:[0,0,0,"아이번"], 40:[0,0,0,"잔나"], 59:[0,0,0,"자르반 4세"], 24:[0,0,0,"잭스"], 126:[0,0,0,"제이스"], 
                202:[0,0,0,"진"], 222:[0,0,0,"징크스"], 145:[0,0,0,"카이사"], 429:[0,0,0,"칼리스타"], 43:[0,0,0,"카르마"], 30:[0,0,0,"카서스"], 38:[0,0,0,"카사딘"], 55:[0,0,0,"카타리나"], 10:[0,0,0,"케일"], 141:[0,0,0,"케인"], 85:[0,0,0,"케넨"], 
                121:[0,0,0,"카직스"], 203:[0,0,0,"킨드레드"], 240:[0,0,0,"클레드"], 96:[0,0,0,"코그모"], 7:[0,0,0,"르블랑"], 64:[0,0,0,"리 신"], 89:[0,0,0,"레오나"], 876:[0,0,0,"릴리아"], 127:[0,0,0,"리산드라"], 236:[0,0,0,"루시안"], 
                117:[0,0,0,"룰루"], 99:[0,0,0,"럭스"], 54:[0,0,0,"말파이트"], 90:[0,0,0,"말자하"], 57:[0,0,0,"마오카이"], 11:[0,0,0,"마스터 이"], 21:[0,0,0,"미스포츈"], 62:[0,0,0,"오공"], 82:[0,0,0,"모데카이저"], 25:[0,0,0,"모르가나"], 
                267:[0,0,0,"나미"], 75:[0,0,0,"나서스"], 111:[0,0,0,"노틸러스"], 518:[0,0,0,"니코"], 76:[0,0,0,"니달리"], 895:[0,0,0,"닐라"], 56:[0,0,0,"녹턴"], 20:[0,0,0,"누누와 윌럼프"], 2:[0,0,0,"올라프"], 61:[0,0,0,"오리아나"], 
                516:[0,0,0,"오른"], 80:[0,0,0,"판테온"], 78:[0,0,0,"뽀삐"], 555:[0,0,0,"파이크"], 246:[0,0,0,"키아나"], 133:[0,0,0,"퀸"], 497:[0,0,0,"라칸"], 33:[0,0,0,"람머스"], 421:[0,0,0,"렉사이"], 526:[0,0,0,"렐"], 888:[0,0,0,"레타나 글라스크"],
                58:[0,0,0,"레넥톤"], 107:[0,0,0,"렝가"], 92:[0,0,0,"리븐"], 68:[0,0,0,"럼블"], 13:[0,0,0,"라이즈"], 360:[0,0,0,"사미라"], 113:[0,0,0,"세주아니"], 235:[0,0,0,"세나"], 147:[0,0,0,"세라핀"], 875:[0,0,0,"세트"], 35:[0,0,0,"샤코"], 
                98:[0,0,0,"쉔"], 102:[0,0,0,"쉬바나"], 27:[0,0,0,"신지드"], 14:[0,0,0,"사이온"], 15:[0,0,0,"시비르"], 72:[0,0,0,"스카너"], 37:[0,0,0,"소나"], 16:[0,0,0,"소라카"], 50:[0,0,0,"스웨인"], 517:[0,0,0,"사일러스"], 134:[0,0,0,"신드라"], 
                223:[0,0,0,"탐 켄치"], 163:[0,0,0,"탈리야"], 91:[0,0,0,"탈론"], 44:[0,0,0,"타릭"], 17:[0,0,0,"티모"], 412:[0,0,0,"쓰레쉬"], 18:[0,0,0,"트리스타나"], 48:[0,0,0,"트런들"], 23:[0,0,0,"트린다미어"], 4:[0,0,0,"트위스티드 페이트"], 
                29:[0,0,0,"트위치"], 77:[0,0,0,"우디르"], 6:[0,0,0,"우르곳"], 110:[0,0,0,"바루스"], 67:[0,0,0,"베인"], 45:[0,0,0,"베이가"], 161:[0,0,0,"벨코즈"], 711:[0,0,0,"벡스"], 254:[0,0,0,"바이"], 234:[0,0,0,"비에고"], 112:[0,0,0,"빅토르"], 
                8:[0,0,0,"블라디미르"], 106:[0,0,0,"볼리베어"], 19:[0,0,0,"워윅"], 498:[0,0,0,"자야"], 101:[0,0,0,"제라스"], 5:[0,0,0,"신 짜오"], 157:[0,0,0,"야스오"], 777:[0,0,0,"요네"], 83:[0,0,0,"요릭"], 350:[0,0,0,"유미"], 154:[0,0,0,"자크"], 
                238:[0,0,0,"제드"], 221:[0,0,0,"제리"], 115:[0,0,0,"직스"], 26:[0,0,0,"질리언"], 142:[0,0,0,"조이"], 143:[0,0,0,"자이라"]}


champ_NameList = ['아트록스', '아리', '아칼리', '아크샨', '알리스타', '아무무', '애니비아', '애니', '아펠리오스', '애쉬', '아우렐리온 솔', '아지르', '바드', '벨베스', '블리츠크랭크', '브랜드', '브라움', '케이틀린', '카밀', '카시오페아', '초가스', '코르키', '다리우스', '다이애나', '드레이븐', '문도 박사', '에코', '엘리스', '이블린', '이즈리얼', '피들스틱', '피오라', '피즈', '갈리오', '갱플랭크', '가렌', '나르', '그라가스', '그레이브즈', '그웬', '헤카림', '하이머딩거', '일라오이', '이렐리아', '아이번', '잔나', '자르반 4세', '잭스', '제이스', '진', '징크스', '카이사', '칼리스타', '카르마', '카서스', '카사딘', '카타리나', '케일', '케인', '케넨', '카직스', '킨드레드', '클레드', '코그모', '르블랑', '리 신', '레오나', '릴리아', '리산드라', '루시안', '룰루', '럭스', '말파이트', '말자하', '마오카이', '마스터 이', '미스포츈', '오공', '모데카이저', '모르가나', '나미', '나서스', '노틸러스', '니코', '니달리', '닐라', '녹턴', '누누와 윌럼프', '올라프', '오리아나', '오른', '판테온', '뽀삐', '파이크', '키아나', '퀸', '라칸', '람머스', '렉사이', '렐', '레타나 글라스크', '레넥톤', '렝가', '리븐', '럼블', '라이즈', '사미라', '세주아니', '세나', '세라핀', '세트', '샤코', '쉔', '쉬바나', '신지드', '사이온', '시비르', '스카너', '소나', '소라카', '스웨인', '사일러스', '신드라', '탐 켄치', '탈리야', '탈론', '타릭', '티모', '쓰레쉬', '트리스타나', '트런들', '트린다미어', '트위스티드 페이트', '트위치', '우디르', '우르곳', '바루스', '베인', '베이가', '벨코즈', '벡스', '바이', '비에고', '빅토르', '블라디미르', '볼리베어', '워윅', '자야', '제라스', '신 짜오', '야스오', '요네', '요릭', '유미', '자크', '제드', '제리', '직스', '질리언', '조이', '자이라']
champ_idList = [266, 103, 84, 166, 12, 32, 34, 1, 523, 22, 136, 268, 432, 200, 53, 63, 201, 51, 164, 69, 31, 42, 122, 131, 119, 36, 245, 60, 28, 81, 9, 114, 105, 3, 41, 86, 150, 79, 104, 887, 120, 74, 420, 39, 427, 40, 59, 24, 126, 202, 222, 145, 429, 43, 30, 38, 55, 10, 141, 85, 121, 203, 240, 96, 7, 64, 89, 876, 127, 236, 117, 99, 54, 90, 57, 11, 21, 62, 82, 25, 267, 75, 111, 518, 76, 895, 56, 20, 2, 61, 516, 80, 78, 555, 246, 133, 497, 33, 421, 526, 888, 58, 107, 92, 68, 13, 360, 113, 235, 147, 875, 35, 98, 102, 27, 14, 15, 72, 37, 16, 50, 517, 134, 223, 163, 91, 44, 17, 412, 18, 48, 23, 4, 29, 77, 6, 110, 67, 45, 161, 711, 254, 234, 112, 8, 106, 19, 498, 101, 5, 157, 777, 83, 350, 154, 238, 221, 115, 26, 142, 143]

#champ_result 돌면서 챔피언(승 0,패 0) 추가하고 본인은 -1
for champ in champ_result:
    for champ_id in champ_idList:
        #print(champ_result[champ])
        if champ != champ_id:
            champ_result[champ].append({champ_id:[0,0]})
        else:
            champ_result[champ].append({champ_id:[-1,-1]})

winCIdList = []     #매치에서 승리한 챔피언id 리스트
loseCIdList = []    #매치에서 패배한 챔피언id 리스트

#매치id를 담는 리스트
matchList = []

#csv 파일 읽어오기(matchId만 list로 저장)
df = pd.read_csv('challengerMatchID.csv', encoding = 'utf-8-sig') #챌린저 유저 정보가 담긴 csv file read
matchList = df['matchId']

#request보낼때마다 +1
count = 0
err_count = list()

#시작시간
start = time.time()

for match in matchList:
    #print(match)
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

        #2분에 최대 100개의 requests
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + match
        res = session.get(URL, headers = {"X-Riot-Token": api_key })

    except requests.exceptions.ConnectionError:
        print('Connection error occured')

    if res.status_code == 200:
        resobj = json.loads(res.text)

        #챔피언id와 승, 패 여부를 알 수 있는 리스트
        #summoner : 매치의 각 소환사

        winCIdList = []     #매치에서 승리한 챔피언id 리스트
        loseCIdList = []    #매치에서 패배한 챔피언id 리스트

        for summoner in resobj["info"]["participants"]:
            #print(summoner["championId"])
            #print(summoner["win"])
            if summoner["win"]:
                tmp = summoner["championId"]
                champ_result[tmp][0] += 1
                winCIdList.append(tmp)
            else:
                tmp = summoner["championId"]
                champ_result[tmp][1] += 1
                #print(summoner["championId"])
                loseCIdList.append(tmp)
        

        #이긴 챔피언 리스트를 돌면서 같이 이긴 챔피언의 win+1
        for winCId_row in winCIdList:   #같은 리스트 내에서 반복
            for winCId_col in winCIdList:   #같은 리스트 내에서 반복
                if winCId_row != winCId_col: #같으면 볼 필요 없음
                    tempCount =0
                    for findCId in champ_result[winCId_row]: #findCId는 266 안의 리스트. 0 0 0 아트록스 {266:[-1,-1]} {103:[0,0]}
                        if tempCount<4:
                            tempCount += 1          #row:266, col:103
                        else:
                            if winCId_col in findCId.keys():
                                findCId[winCId_col][0] +=1
        #진 챔피언 리스트를 돌면서 같이 진 챔피언의 lose+1
        for loseCId_row in loseCIdList:   #같은 리스트 내에서 반복
            for loseCId_col in loseCIdList:   #같은 리스트 내에서 반복
                if loseCId_row != loseCId_col: #같으면 볼 필요 없음
                    tempCount =0
                    for findCId in champ_result[loseCId_row]: 
                        if tempCount<4:
                            tempCount += 1          
                        else:
                            if loseCId_col in findCId.keys():
                                findCId[loseCId_col][1] +=1

        for color in [0,1]:
            #밴된 챔피언을 확인하는 리스트. 블루팀이 0 레드팀이 1
            for i in resobj["info"]["teams"][color]["bans"]:
                if i["championId"] != -1:
                    champ_result[i["championId"]][2] += 1

        count += 1
        print("Done "+str(count) + "/" + str(matchCount))
        #time.sleep(1.2)
    else:
        err_count.append(count)
        count += 1
        print("error occured. check your api key or input")    

#print(champ_result)

#champ_result csv로 저장. column은 championName, championId, win, lose, banned 5개
cName = []
cId = []
cWin = []
cLose = []
cBanned = []

#결과물을 리스트에 넣음
for champ in champ_result:
    cId.append(champ)   #return key
    cName.append(champ_result[champ][3])
    cWin.append(champ_result[champ][0])
    cLose.append(champ_result[champ][1])
    cBanned.append(champ_result[champ][2])

#데이터프레임에 저장
df = pd.DataFrame(cName, columns = ['championName'])
df['championId'] = cId
df['Win'] = cWin
df['Lose'] = cLose
df['Banned'] = cBanned

#챔피언 col이 들어있는 칸이 4~164이다. 
for champ_col in range(4,165):
    cwList=[]   #이긴 챔피언 리스트
    clList=[]   #진 챔피언 리스트
    for champ_row in champ_result:  #champ_row: 266: [0,0,0,'아트록스', {266: [-1,-1]},...]
        tmp = list(champ_result[champ_row][champ_col].values())
        cwList.append(tmp[0][0])
        clList.append(tmp[0][1])
    #돌았으면 df에 저장. 챔프이름(승) 챔프이름(패) 이렇게 두개 저장
    colWName = champ_NameList[champ_col-4] + "(승)"
    colLName = champ_NameList[champ_col-4] + "(패)"
    df[colWName] = cwList
    df[colLName] = clList

#csv에 저장
df.to_csv("MatchResult.csv", index = False, encoding = 'utf-8-sig')

#에러를 일으킨 매치 아이디list 출력
print(err_count)