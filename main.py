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
		info[new_id] = i
		oder_list[i].append((new_id, dst))

#車の位置を記録いていく
vehicle = []

#車に積んである荷物を記録していく
#key: 目的地, value: 注文idのリスト
luggage = {key: [] for key in range(V)}


LEVEL = 4
#最適解を探索する
#時間tまでの評価関数efuncを比較して一番高いものを返す
def search(t, level, score):		#t: 時間, level: 読んでいる深さ, score: 得点
	#t >= Tmax のときscoreを返す
	if t >= T:
		return score

	#車がお店にいるとき
	if vehicle[level] == 0:
		#level >= 読み切る深さ のとき得点を計算して返す
		if level >= LEVEL:
			return score
		#時間tまでに受けた注文idを受け取る
		for i in range(t):
			for oder in oder_list[i]:
				luggage[oder[1]].append(oder[0])
#既に配達済みの荷物まで受け取ってしまう
		#配達場所(複数の目的地)までの最短経路を計算する
		#max = -無限
		#comp = search(配達に行く場合)
		#comp > max のとき max = comp
		#comp = search(店にとどまる場合)
		#comp > max のとき now_score = comp
		#return max

	#車が今積んでいるすべての荷物を配達完了したとき
	#得点計算
	#level >= 読み切る深さ のとき得点を計算して返す
	#return search(店に戻る, 計算した得点を引数に渡す)

	#車が途中の配達まで完了したとき
	#得点計算
	#level >= 読み切る深さ のとき得点を計算して返す
	#max = -無限
	#comp = search(店に戻る, 計算した得点を引数に渡す)
	#comp > max のとき max = comp
	#comp = search(次の配達場所に向かう, 計算した得点を引数に渡す)
	#return max

	#search関数が呼ばれた時に車がお店にいるとは限らない
	#車の位置を記憶しておくものが必要
	#車に何が積んであるのか記録しておくものが必要
	#車が何を選択したかを記憶するものが必要

# insert your code here to get more meaningful output
# all stay
for i in range(T) :
	print (-1)

