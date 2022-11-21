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
승-패인데
승-패가 절댓값으로 10 넘어가면 가중치 감소-> 판수가 너무 커졌을 때 비슷한데도 상성이 너무 안좋게 나오지 않게 하기 위함

두 챔피언과의 매치 승,패만 있음

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
df = pd.read_csv("MatchResult_12.20.csv", encoding='utf-8-sig')
#print(df.loc[0][0]) #행 열

for i in range(champ_Count):
    champ = []
    champ.append(df.loc[i][0])              #챔피언 이름
    champ_NameList.append(df.loc[i][0])
    for j in range(champ_Count):
        champ.append(df.loc[i][j*5+8])      #vs챔피언(승)
        champ.append(df.loc[i][j*5+9])      #vs챔피언(패)
    champ_Info.append(champ)

maxValue = 0
minValue = 0

winRate_weight = 0.85
banRate_weight = 0.0025

weight = []

#print(champ_Info)

for i in range(champ_Count):
    for j in range(champ_Count):
        if i!=j:
            edge = []
            edge.append(champ_Info[i][0])
            edge.append(champ_Info[j][0])
            champ_Edge.append(edge)

            total = champ_Info[i][j*2+1]+champ_Info[i][j*2+2]   #판수
            margin = champ_Info[i][j*2+1]-champ_Info[i][j*2+2]  #vs챔피언(승), vs챔피언(패)
            
            if total > 30:
                margin = margin/2
            if total > 50:
                margin = margin/2
            if margin > 100:
                margin = margin/2
                
            value = margin
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
        normalized_value = 0.02
    champ_Edge[i].append(normalized_value)
print(len(champ_Edge))
#print(weight)

Graph = nx.DiGraph()    #directed graph

Graph.add_nodes_from(champ_NameList)
for i in range(len(champ_Edge)):
    Graph.add_edge(champ_Edge[i][0], champ_Edge[i][1], weight=champ_Edge[i][2])
nx.write_gexf(Graph, "ChampGraph_12.20_counter.gexf")