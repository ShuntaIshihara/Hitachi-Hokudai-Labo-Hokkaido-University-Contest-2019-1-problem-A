import sys
import copy
# recieve |V| and |E|
with open('testcase.in', 'r') as f:	
	line = f.readline()
	V, E = map(int, line.split())
	es = [[] for i in range(V)]
	
	for i in range(E):
		line = f.readline()
		# recieve edges
		#es[point][edgenumber]: 頂点pointにedgenumber本の辺がある
		#値はつながっている頂点とその距離
		a, b, c = map(int, line.split())
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
	line = f.readline()	
	T = int(line)
	# recieve info
	
	#受け取った情報をリストアップしていく
	#oder_time: key: 注文id, value: 注文時間t
	oder_time = {}
	
	#oder_list[t][i]: 時間tに発生したi番目の注文情報
	oder_list = [[] for i in range(T)]
	
	for i in range(T):
		line = f.readline()
		Nnew = int(line)
		for j in range(Nnew):
			line = f.readline()
			new_id, dst = map(int, line.split())
			oder_time[new_id] = i
			oder_list[i].append((new_id, dst-1))

#配達に向かう目的地をリストに入れる
def get_destination(d, l):
	for i in range(V):
		if l[i]:
			d.append(i)

#時間s+1からtまでに注文された荷物を受け取る関数
def get_luggage(l, s, t):
	for i in range(s+1, t+1):
		for oder in oder_list[i]:
			l[oder[1]].append(oder[0])
	
	return t


#配達場所までの最短経路になるようにソートする関数
def get_route(start, start_index, d):
	if start_index >= len(d)-1:
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

	get_route(d[start_index], start_index+1, d)

LEVEL = 4		#読みきる深さ
#最適解を探索する
#t: 時間,  level: 読んでいる深さ, vehicle: 車の位置, score: 得点, shipping: 最後にお店に立ち寄った時間, dst_list: 配達に向かう順番, luggage: 荷物 
def search(t, level, vehicle, score, shipping, dst_list, luggage):
	#t >= Tmax のときscoreを返す
	if t >= T:
		return score

	#levelが読みきる深さになったとき
	if level >= LEVEL:
		return score

	luggage_copy = copy.deepcopy(luggage)
	dst_list_copy = copy.copy(dst_list)
	#車がお店にいるとき
	if vehicle == 0:

		#時間tまでに受けた注文idを受け取る
		shipping = get_luggage(luggage_copy, shipping, t)

		#配達場所(複数の目的地)までの最短経路を計算する
		#もしdst_listが空ではなかったら空にする
		if dst_list_copy != None:
			dst_list_copy.clear()

		#配達に向かう場所を記憶する
		get_destination(dst_list_copy, luggage_copy)

		#dst_listが最短経路でソートされる
		get_route(0, 0, dst_list_copy)

		#comp = search(配達に行く場合)
		max_score = sys.maxsize
		if dst_list_copy:
			max_score = search(t+shortest_time[vehicle][dst_list_copy[0]], level+1, dst_list_copy[0], score, shipping, dst_list_copy, luggage_copy)
		#comp = search(店にとどまる場合)
		comp = search(t+1, level+1, vehicle, score, shipping, dst_list_copy, luggage_copy)
		#comp > max のとき now_score = comp
		if comp > max_score:
			max_score = comp
		#return max
		return max_score


	#車が今積んでいるすべての荷物を配達完了したとき
	elif dst_list_copy.index(vehicle) == len(dst_list_copy) - 1:
		for i in luggage_copy[vehicle]:
			#得点計算
			waitingTime = t - oder_time[i]
			score += T*T - waitingTime*waitingTime
		luggage_copy[vehicle].clear()

		#return search(店に戻る, 計算した得点を引数に渡す)
		return search(t+shortest_time[vehicle][0], level+1, 0, score, shipping, dst_list_copy, luggage_copy)

	#車が途中の配達まで完了したとき
	else:
		for i in luggage_copy[vehicle]:
			#得点計算
			waitingTime = t - oder_time[i]
			score += T*T - waitingTime*waitingTime
		luggage_copy[vehicle].clear()

		#comp = search(次の配達場所に向かう, 計算した得点を引数に渡す)
		max_score = search(t+shortest_time[vehicle][dst_list_copy[dst_list_copy.index(vehicle)+1]], level+1, dst_list_copy[dst_list_copy.index(vehicle)+1], score, shipping, dst_list_copy, luggage_copy)

		#comp = search(店に戻る, 計算した得点を引数に渡す)
		comp = search(t+shortest_time[vehicle][0], level+1, 0, score, shipping, dst_list_copy, luggage_copy)
		#comp > max のとき max = comp
		if comp > max_score:
			max_score = comp
		#return max
		return max_score

#車に積んである荷物を記録していく
#key: 目的地, value: 注文idのリスト
real_l = {key: [] for key in range(V)}
#車の目的地を記録していく
real_d = []
#index
index = 0
#次の行動
next_move = -1
#次の目的地
next_dst = 0
#車の現在地
real_v = 0
#最後に店に訪れた時間
shipping_time = -1
#次の頂点につくまでのカウンター
count = sys.maxsize

situation = 1
# insert your code here to get more meaningful output
# all stay
with open('test_case.out', 'w') as f:
	for i in range(T) :
		if count <= 0:
			if next_move != -2:
				real_v = next_move
				if real_v != next_dst:
					next_move = shortest_route[real_v][next_dst][0]
					count = shortest_time[real_v][next_move]
	#次の目的地と車の現在地が等しいとき
		if real_v == next_dst:
			count = sys.maxsize
			#車が店にいるとき
			if real_v == 0:
				index = 0
				#荷物を受け取る関数
				shipping_time = get_luggage(real_l, shipping_time, i)
				#新しく目的地のリストを作る
				if real_d != None:
					real_d.clear()
				get_destination(real_d, real_l)
				#複数の目的地のルートを受け取る関数
				get_route(0, 0, real_d)
				#とどまる場合
				max_score = search(i+1, 0, real_v, 0, shipping_time, real_d, real_l)
				next_dst = 0
				next_move = -2
				count = 0
				#いく場合
				comp = -1
				if real_d:
					comp = search(i+shortest_time[real_v][real_d[index]], 0, real_d[index], 0, shipping_time, real_d, real_l)
				if comp > max_score:
					next_dst = real_d[index]
					next_move = shortest_route[real_v][next_dst][0]
					count = shortest_time[real_v][next_move]
					index += 1
			#車が今ある荷物をすべて配達したとき
			elif index >= len(real_d) - 1:
				real_d.clear()
				real_l[real_v].clear()
				next_dst = 0
				next_move = shortest_route[real_v][next_dst][0]
				count = shortest_time[real_v][next_move]
			#車が途中の配達場所まで配達完了したとき
			else:
				real_l[real_v].clear()
				#店にもどる
				max_score = search(i+shortest_time[real_v][0], 0, 0, 0, shipping_time, real_d, real_l)
				next_dst = 0
				next_move = shortest_route[real_v][next_dst][0]
				count = shortest_time[real_v][next_move]
				#次の目的地に行く
				comp = search(i+shortest_time[real_v][real_d[index]], 0, real_d[index], 0, shipping_time, real_d, real_l)
				if comp > max_score:
					next_dst = real_d[index]
					next_move = shortest_route[real_v][next_dst][0]
					count = shortest_time[real_v][next_move]
					index += 1
	
			#次の行動を出力する
			count -= 1
			print(next_move+1, file=f)
	
		#次の頂点まで移動中のとき
		else:
			count -= 1
			print(next_move+1, file=f)

		if i >= T/100 * situation:
			print('=', end="")
			situation += 1
