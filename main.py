import sys
import copy
# recieve |V| and |E|
V, E = map(int, input().split())
es = [[] for i in range(V)]

for i in range(E):

	# recieve edges
	#es[point][edgenumber]: 頂点pointにedgenumber本の辺がある
	#値はつながっている頂点とその距離
	a, b, c = map(int, input().split())
	a, b = a-1, b-1
	es[a].append((b,c))
	es[b].append((a,c))

#頂点iから頂点j(0 <= i <= V-1, 0 <= j <= V-1)の最短時間をリストアップする
#shortest_time[i][j]: 頂点iから頂点jまでの最短時間が記録されている
shortest_time = [[sys.maxsize for j in range(V)] for i in range(V)]

#頂点iから頂点j(0 <= i <= V-1, 0 <= j <= V-1)の最短経路をリストアップする
#shortest_route[i][j]: 頂点iから頂点jまでの経路のリストが取得できる
shortest_route = [[[] for j in range(V)] for i in range(V)]

#最短時間と最短経路をリストアップする関数を作る
def make_shortest_time_and_route(current, point, t, ic):
	#既に追加されている時間以上であればバックする
	if shortest_time[current][point] < t:
		return
	
	#行き先が自分の頂点であるときの距離は0にする
	if current == point:
		shortest_time[current][point] = 0
	
	for edge_tuple in es[point]:
		if shortest_time[current][edge_tuple[0]] > t+edge_tuple[1]:
			#既に追加されている時間よりも小さかったら代入する
			shortest_time[current][edge_tuple[0]] = t+edge_tuple[1]

			#途中経路を記録していく	
			ic.append(edge_tuple[0])

			#最短時間でいける経路を記録していく
			#新しく最短経路が見つかれば上書きされる
			shortest_route[current][edge_tuple[0]] = copy.copy(ic)

			#再帰呼び出し
			make_shortest_time_and_route(current, edge_tuple[0], t+edge_tuple[1], ic)

			#新しい経路のために古いものを削除しておく
			del ic[-1]
			
for i in range(V):
	interchange = []
	make_shortest_time_and_route(i, i, 0, interchange)

T = int(input())
# recieve info
#受け取った情報をリストアップしていく
#info[t][n]: 時間tにおける注文n個の注文情報が記録される
info = [[] for i in range(T)]
for i in range(T):
	Nnew = int(input())
	for j in range(Nnew):
		new_id, dst = map(int, input().split())
		info[i].append((new_id, dst))

# insert your code here to get more meaningful output
# all stay
for i in range(T) :
	print (-1)

