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
#oder_time: key: 注文id, value: 注文時間t
oder_time = {}

#oder_list[t][i]: 時間tに発生したi番目の注文情報
oder_list = [[] for i in range(T)]

for i in range(T):
	Nnew = int(input())
	for j in range(Nnew):
		new_id, dst = map(int, input().split())
		oder_time[new_id] = i
		oder_list[i].append((new_id, dst))




#配達場所までの最短経路になるようにソートする関数
def search_shortest_route(start, start_index, d):
	if start_index >= len(d):
		return

	min = sys.maxsize
	v = -1
	for i in range(start_index, len(d)):
		if min > shortest_time[start][d[i]]:
			min = shortest_time[start][d[i]]
			v = i
	
	w = d[start_index]
	d[start_index] = d[v]
	d[v] = w

	search_shortest_route(v, start_index+1, d)

#車に積んである荷物を記録していく
#key: 目的地, value: 注文idのリスト
luggage = {key: [] for key in range(V)}	
LEVEL = 4		#読みきる深さ
next_move = -1	#車が次に取る行動

#最適解を探索する
#t: 時間,  level: 読んでいる深さ, vehicle: 車の位置, score: 得点, shipping: 最後にお店に立ち寄った時間, dst_list: 配達に向かう順番, luggage: 荷物 
def search(t, level, vehicle, score, shipping, dst_list, luggage):
	#t >= Tmax のときscoreを返す
	if t >= T:
		return score

	#車がお店にいるとき
	if vehicle == 0:
		#level >= 読み切る深さ のとき得点を計算して返す
		if level >= LEVEL:
			return score

		#時間tまでに受けた注文idを受け取る
		for i in range(sipping+1, t+1):
			for oder in oder_list[i]:
				luggage[oder[1]].append(oder[0])
		luggage_copy = copy.deepcopy(luggage)

		#配達場所(複数の目的地)までの最短経路を計算する
		#もしdst_listが空ではなかったら空にする
		if dst_list != None:
			dst_list.clear()

		#配達に向かう場所を記憶する
		for i in range(V):
			if luggage[i]:
				dst_list.append(i)

		#dst_listが最短経路でソートされる
		search_shortest_route(0, 0, dst_list)		
		dst_list_copy = copy.copy(dst_list)

		#comp = search(配達に行く場合)
		max_score = search(t+shortest_time[vehicle][dst_list[0]], level+1, dst_list[0], score, t, dst_list_copy, luggage_copy)
		if level == 0:
			next_move = dst_list[0]
		#comp = search(店にとどまる場合)
		comp = search(t+1, level+1, vehicle, score, t, dst_list_copy, luggage_copy)
		#comp > max のとき now_score = comp
		if comp > max_score:
			max_score = comp
			if level == 0:
				next_move = -1
		#return max
		return max_score


	#車が今積んでいるすべての荷物を配達完了したとき
	elif dst_list.index(vehicle) == len(dst_list) - 1:
		for i in luggage[vehicle]:
			#得点計算
			waitinTime = t - oder_time[i]
			score += T*T - waitingTime*waitingTime
		luggage[vehicle].clear()

		#level >= 読み切る深さ のとき得点を計算して返す
		if level >= LEVEL:
			return score:

		#return search(店に戻る, 計算した得点を引数に渡す)
		dst_list_copy = copy.copy(dst_list)
		luggage_copy = copy.deepcopy(luggage)
		if level == 0:
			next_move = 0
		return search(t+shortest_time[vehicle][0], level+1, 0, score, shipping, dst_list_copy, luggage_copy)

	#車が途中の配達まで完了したとき
	else:
		for i in luggage[vehicle]:
			#得点計算
			waitingTime = t - oder_time[i]
			score += T*T - waitingTime*waitingTime
		luggage[vehicle].clear()

		#level >= 読み切る深さ のとき得点を計算して返す
		if level >= LEVEL:
			return score

		dst_list_copy = copy.copy(dst_list)
		luggage_copy = copy.deepcopy(luggage)

		#comp = search(次の配達場所に向かう, 計算した得点を引数に渡す)
		max_score = search(t+shortest_time[vehicle][dst_list[dst_list.index(vehicle)+1]], level+1, dst_list[dst_list.index(vehicle)+1], score, shipping, dst_list_copy, luggage_copy)
		
		if level == 0:
			next_move = dst_list[dst_list.index(vehicle)+1]

		#comp = search(店に戻る, 計算した得点を引数に渡す)
		comp = search(t+shortest_time[vehicle][0], level+1, 0, score, shipping, dst_list_copy, luggage_copy)
		#comp > max のとき max = comp
		if comp > max_score:
			max_score = comp
		#return max
		return max_score


# insert your code here to get more meaningful output
# all stay
for i in range(T) :
	#返り値: next_move
	start_search(i, score)
