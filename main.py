import sys
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

#頂点iから頂点j(0 <= i <= V, 0 <= j <= V)の最短時間をリストアップする
#shortest_time[i][j]: 頂点iから頂点jまでの最短距離が記録されている
shortest_time = [[sys.maxsize for j in range(V)] for i in range(V)]
def make_shortest_time(current, point, t):
	#既に追加されている時間以上であればバックする
	if shortest_time[current][point] <= t:
		return
	
	for edge_tuple in es[point]:
		print(edge_tuple[0])
		#既に追加されている時間よりも小さかったら代入する
		if shortest_time[current][edge_tuple[0]] > t+edge_tuple[1]:
			shortest_time[current][edge_tuple[0]] = t+edge_tuple[1]
			make_shortest_time(current, edge_tuple[0], t+edge_tuple[1])
			
for i in range(V):
	make_shortest_time(i, i, 0)

for i in shortest_time:
	print(i) 
	

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

