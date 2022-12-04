# KHU2022-CapstoneDesign2-LCI

경희대학교 2022년 2학기 캡스톤디자인2 <br/>
컴퓨터공학과 김형석 2016104118 <br/>
hsuper189@khu.ac.kr <br/>

## 주제
Graph Centrality를 이용한 리그 오브 레전드 챔피언 영향력 분석 
<br/><br/>

## 요약
전세계에서 가장 많이 플레이되고 있는 게임 중 하나인 리그 오브 레전드에서 티어(tier)가 높은 챔피언을 고르는 것은 게임 승리의 지름길이다. 한편, 리그 오브 레전드는 한 달에 두 번 정도로 패치가 잦으며, 잦은 패치로 챔피언의 티어가 급변한다. 따라서, 리그 오브 레전드 유저들의 챔피언 티어에 대한 수요는 꾸준하다. 본 연구에서는 Weighted Degree Centrality와 Betweenness Centrality를 이용해 최근 일주일 간 리그 오브 레전드 랭크 게임에서 챔피언들의 영향력을 분석하였다. 그리고, 에지 가중치를 통해 특정 챔피언과 함께 플레이한 다른 챔피언과의 시너지(synergy)와 상대로 만난 다른 챔피언과의 상성까지도 분석해 유저들에게 게임에서 승리할 수 있는, 좋은 챔피언을 제시하고자 한다.
<br/><br/>

## 프로그램 및 모듈 설치
#### 1. API key 발급
```
https://developer.riotgames.com/
```
데이터 수집을 위해서는 Riot API를 이용해야 한다. <br/>
Riot API를 이용하기 위해서는 Riot Developer Portal에서 API key를 발급받아야 한다.<br/>
#### 2. Graph
```
pip install pandas
pip install networkx
```
그래프 생성을 위해서 pandas와 networkx 를 설치한다.<br/>
#### 3. Gephi
```
https://gephi.org/
```
그래프 시각화를 위해 Gephi 홈페이지에서 Gephi를 다운로드받아 설치한다.
<br/><br/>

## 그래프 시각화
![image](https://user-images.githubusercontent.com/30518853/205503307-ba68bb6c-84cf-4562-800e-14bff32f7294.PNG)



