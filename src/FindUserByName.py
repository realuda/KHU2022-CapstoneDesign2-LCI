import requests

api_key = "RGAPI-39b371e9-77a6-4baa-bb67-629c0dcc7ba0"


name = input("소환사의 닉네임을 입력해주세요: ")
URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name
res = requests.get(URL, headers={"X-Riot-Token": api_key})
if res.status_code == 200:
    #코드가 200일때
    print(res.text)
else:
    # 코드가 200이 아닐때(즉 찾는 닉네임이 없을때)
    print("소환사가 존재하지 않습니다")