'''
그래프 생성하기
node: 챔피언
edge: 챔피언간 승,패 
edge weight: 일단 챔피언 승-패로 우선 그래프 생성부터?
                이후에 밴률, 픽률 다 고려해서 최소 0, 최대 1로 정규화

먼저 데이터 불러와서 가로로 읽기
list: 챔피언이름/총 판 수/밴수/챔피언별 승패/... 로 저장

기존 데이터
챔피언이름  cId  Win    Lose    Banned  ...

저장 데이터
챔피언이름  총판수 밴수 아트승 아트패 아리승 아리패

-Graph(networkx)
networkx Graph 클래스 자체가 undirected임. DiGraph는 directed. self loof도 가능하니 조심할 것

-Node
챔피언 이름

-Edge
add_edge : edge1, edge2, weight

-Weight
승률>픽률>밴률
승률: 50% 기준으로 +-%  승률을 픽률의 3배정도 가중치로 잡음
픽률: n%               픽률을 밴률의 5배정도 가중치로 잡음
밴률: m%    

두 챔피언과의 매치 승,패만 있음

두 챔피언 경기수의 합은 한 챔피언 게임 수 *4 (팀원이 4명이라서)
전 챔피언 다 합치면 전 챔피언 경기 수는? 전 매치 수 * 10. 양방향이니 /2
다 합쳐서 1로 만들기
두 챔프 밴 수 합/전체 게임 수/10(10개 밴)/2(챔프 둘) + (두 챔프 경기 수 합)/전체 게임 수/20*5 + (승-패)/두 챔피언 게임 수/20*15
(3010+37)/5414/20, 1788/5414/20*5, -1/(n)/20*15
픽률 50%에 승-패 마진이 낮으면?
승률 50%이상이면 weight 업
-정규화 
(value - min)/(max-min)
'''
import pandas as pd
import networkx as nx

match_Count = 5414 #전체 매치수
champ_Count = 161 

#챔피언 이름, 수
champ_NameList = []
#edge list [i][0]: edge1 [i][1]: edge2 [i][2]: weight
champ_Edge = []
#MAIN
champ_Info = []
df = pd.read_csv("MatchResult.csv", encoding='utf-8-sig')
#print(df.loc[0][0]) #행 열

for i in range(champ_Count):
    champ = []
    champ.append(df.loc[i][0])              #챔피언 이름
    champ_NameList.append(df.loc[i][0])
    #champ.append(df.loc[i][2]+df.loc[i][3]) #총 판 수
    #champ.append(df.loc[i][4])              #밴 수
    for j in range(champ_Count):
        champ.append(df.loc[i][j*3+5])      #챔피언(승)
        champ.append(df.loc[i][j*3+6])      #챔피언(패)
        champ.append(df.loc[i][j*3+7])      #챔피언(밴)
    champ_Info.append(champ)

maxValue = 0
minValue = 0

#pick_bonus = 5      #픽률 가중치
#winRate_bonus = 15  #승률 가중치
winRate_weight = 0.85
banRate_weight = 0.0025

weight = []

#print(champ_Info)

for i in range(champ_Count):
    for j in range(i+1, champ_Count):
        edge = []
        edge.append(champ_Info[i][0])
        edge.append(champ_Info[j][0])
        champ_Edge.append(edge)

        value = champ_Info[i][j*3+1]-champ_Info[i][j*3+2]*winRate_weight+champ_Info[i][j*3+3]*banRate_weight
        #print(value)
        if value > maxValue:
            maxValue = value
        elif value < minValue:
            minValue = value

        weight.append(value)
#print(len(weight))
for i in range(len(weight)):
    normalized_value = (weight[i]-minValue) / (maxValue-minValue)
    if(normalized_value == 0):
        normalized_value = 0.1

    normalized_value = 1 / normalized_value
    champ_Edge[i].append(normalized_value)
print(len(champ_Edge))
#print(weight)

Graph = nx.Graph()
Graph.add_nodes_from(champ_NameList)

edge_list = []

for i in range(len(champ_Edge)):
    edge_list.append((champ_Edge[i][0], champ_Edge[i][1], {'weight':champ_Edge[i][2]}))

Graph.add_edges_from(edge_list)
betweenness = nx.betweenness_centrality(Graph, weight='weight')

print(betweenness)